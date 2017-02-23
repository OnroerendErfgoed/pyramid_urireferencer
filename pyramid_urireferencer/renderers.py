# -*- coding: utf-8 -*-


from pyramid.renderers import JSON

from pyramid_urireferencer.models import (
    RegistryResponse,
    ApplicationResponse
)

json_renderer = JSON()


def registry_adapter(obj, request):
    """
    Adapter for rendering a :class:`pyramid_urireferencer.models.RegistryResponse` to json.

    :param pyramid_urireferencer.models.RegistryResponse obj: The response to be rendered.
    :rtype: :class:`dict`
    """
    return {
        'query_uri': obj.query_uri,
        'success': obj.success,
        'has_references': obj.has_references,
        'count': obj.count,
        'applications': [{
                             'title': a.title,
                             'uri': a.uri,
                             'service_url': a.service_url,
                             'success': a.success,
                             'has_references': a.has_references,
                             'count': a.count,
                             'items': [{
                                           'uri': i.uri,
                                           'title': i.title
                                       } for i in a.items] if a.items is not None else None
                         } for a in obj.applications] if obj.applications is not None else None
    }


def application_adapter(obj, request):
    """
    Adapter for rendering a :class:`pyramid_urireferencer.models.ApplicationResponse` to json.

    :param pyramid_urireferencer.models.ApplicationResponse obj: The response to be rendered.
    :rtype: :class:`dict`
    """
    return {
        'title': obj.title,
        'uri': obj.uri,
        'service_url': obj.service_url,
        'success': obj.success,
        'has_references': obj.has_references,
        'count': obj.count,
        'items': [{
                      'uri': i.uri,
                      'title': i.title
                  } for i in obj.items] if obj.items is not None else None
    }


json_renderer.add_adapter(RegistryResponse, registry_adapter)
json_renderer.add_adapter(ApplicationResponse, application_adapter)
