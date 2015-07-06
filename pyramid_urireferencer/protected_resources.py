# -*- coding: utf-8 -*-
'''
Thids module is used when blocking operations on a certain uri
that might be used in external applications.
.. versionadded:: 0.4.0
'''

from pyramid.httpexceptions import (
    HTTPInternalServerError,
    HTTPConflict)

import pyramid_urireferencer


def protected_operation(fn):
    '''
    Use this decorator to prevent an operation from being executed
    when the related uri resource is still in use.
    :raises pyramid.httpexceptions.HTTPConflict: Signals that we don't want to 
        delete a certain URI because it's still in use somewhere else.
    :raises pyramid.httpexceptions.HTTPInternalServerError: Raised when we were
        unable to check that the URI is no longer being used.
    '''
    def advice(parent_object, *args, **kw):
        id = parent_object.request.matchdict['id']
        referencer = pyramid_urireferencer.get_referencer(parent_object.request.registry)
        uri = parent_object.uri_template.format(id)
        registery_response = referencer.is_referenced(uri)
        if registery_response.has_references:
            raise HTTPConflict(
                detail="Urireferencer: The uri {0} is still in use by other applications: {1}".
                    format(uri, ', '.join([app_response.title for app_response in registery_response.applications
                                           if app_response.has_references])))
        elif not registery_response.success:
            raise HTTPInternalServerError(
                detail="Urireferencer: Something went wrong while retrieving references of the uri {0}".format(uri))
        return fn(parent_object, *args, **kw)

    return advice