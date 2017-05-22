# -*- coding: utf-8 -*-
"""
Thids module is used when blocking operations on a certain uri
that might be used in external applications.
.. versionadded:: 0.4.0
"""
import logging

from pyramid.httpexceptions import (
    HTTPInternalServerError,
    HTTPConflict)
from webob import Response

import pyramid_urireferencer

log = logging.getLogger(__name__)


def protected_operation(fn):
    """
    Use this decorator to prevent an operation from being executed
    when the related uri resource is still in use.
    The parent_object must contain:
        * a request
            * with a registry.queryUtility(IReferencer)
    :raises pyramid.httpexceptions.HTTPConflict: Signals that we don't want to
        delete a certain URI because it's still in use somewhere else.
    :raises pyramid.httpexceptions.HTTPInternalServerError: Raised when we were
        unable to check that the URI is no longer being used.
    """

    def advice(parent_object, *args, **kw):
        referencer = pyramid_urireferencer.get_referencer(parent_object.request.registry)
        uri = referencer.get_uri(parent_object.request)
        registery_response = referencer.is_referenced(uri)
        if registery_response.has_references:
            if parent_object.request.headers.get("Accept", None) == "application/json":
                response = Response()
                response.status_code = 409
                response_json = {
                    "message": "The uri {0} is still in use by other applications. "
                               "A total of {1} references have been found.".format(uri, registery_response.count),
                    "errors": [],
                    "registry_response": registery_response.to_json()
                }
                for app_response in registery_response.applications:
                    if app_response.has_references:
                        error_string = "{0}: {1} references found, such as {2}" \
                            .format(app_response.uri,
                                    app_response.count,
                                    ', '.join([i.uri for i in app_response.items]))
                        response_json["errors"].append(error_string)
                    response.json_body = response_json
                    response.content_type = 'application/json'
                return response
            else:
                raise HTTPConflict(
                    detail="Urireferencer: The uri {0} is still in use by other applications. "
                           "A total of {1} references have been found "
                           "in the following applications: {2}".format(uri, registery_response.count,
                                                                       ', '.join([app_response.title for app_response in
                                                                                  registery_response.applications
                                                                                  if app_response.has_references])))
        elif not registery_response.success:
            if parent_object.request.headers.get("Accept", None) == "application/json":
                response = Response()
                response.status_code = 500
                response_json = {
                    "message": "Unable to verify the uri {0} is no longer being used.".format(uri),
                    "errors": [],
                    "registry_response": registery_response.to_json()
                }
                for app_response in registery_response.applications:
                    if not app_response.success:
                        response_json["errors"].append(
                            "{}: Could not verify the uri is no longer being used.".format(app_response.uri))
                response.json_body = response_json
                response.content_type = 'application/json'
                return response
            else:
                log.error("Urireferencer: Unable to verify the uri {0} is no longer being used. "
                          "Could not verify with {1}".format(uri, ', '
                                                             .join(["{0} ({1})".format(app_response.uri,
                                                                                       app_response.service_url)
                                                                    for app_response
                                                                    in registery_response.applications if
                                                                    not app_response.success])))
                raise HTTPInternalServerError(
                    detail="Urireferencer: Unable to verify the uri {0} is no longer being used. "
                           "Could not verify with {1}".format(uri, ', '.join([app_response.uri for app_response
                                                                              in registery_response.applications if
                                                                              not app_response.success])))
        return fn(parent_object, *args, **kw)

    return advice
