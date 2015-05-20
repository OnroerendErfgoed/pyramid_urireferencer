# -*- coding: utf-8 -*-


from pyramid.renderers import JSON

from pyramid_urireferencer.models import (
    RegistryResponse,
    ApplicationResponse
)


json_renderer = JSON()

def registry_adapter(obj, request):
    '''
    Adapter for rendering a :class:`pyramid_urireferencer.models.RegistryResponse` to json.

    :param pyramid_urireferencer.models.RegistryResponse obj: The response to be rendered.
    :rtype: :class:`dict`
    '''
    return {
        'query_uri': obj.uri,
        'success': obj.success,
        'has_references': obj.has_references,
        'count': obj.count,
        'applications': [
            {
                'title': a.title,
                'uri': a.uri,
                'url': a.url,
                'success': a.success,
                'has_references': a.has_references,
                'count': a.count,
                'items': [
                    {
                        'uri': i.uri,
                        'title': i.title
                    } for i in a.items
                ]

            } for a in obj.applications
        ]
    }

def application_adapter(obj, request):
    '''
    Adapter for rendering a :class:`pyramid_urireferencer.models.ApplicationResponse` to json.

    :param pyramid_urireferencer.models.ApplicationResponse obj: The response to be rendered.
    :rtype: :class:`dict`
    '''
    return {
        'title': obj.title,
        'uri': obj.uri,
        'url': obj.url,
        'success': obj.success,
        'has_references': obj.has_references,
        'count': obj.count,
        'items': [
            {
                'uri': i.uri,
                'title': i.title
            } for i in obj.items
        ]
    }

json_renderer.add_adapter(RegistryResponse, registry_adapter)
json_renderer.add_adapter(ApplicationResponse, application_adapter)