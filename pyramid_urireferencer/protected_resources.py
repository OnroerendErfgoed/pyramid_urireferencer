# -*- coding: utf-8 -*-
from pyramid.httpexceptions import (
    HTTPInternalServerError,
    HTTPConflict)

import pyramid_urireferencer

'''
Thid module is used when blocking operations on a certain uri
that might be used in external applications.
'''



def protected_operation(fn):
    '''
    use this decorator to prevent an operation from being executed
    when the related uri resource is still in use
    '''

    def advice(parent_object, *args, **kw):
        id = parent_object.request.matchdict['id']
        referencer = pyramid_urireferencer.get_referencer(parent_object.request.registry)
        uri = parent_object.uri_template.format(id)
        registery_response = referencer.is_referenced(uri)
        if not registery_response.success:
            raise HTTPInternalServerError(
                detail="Urireferencer: Something goes wrong while retrieving references of the uri {0}".format(uri))
        if registery_response.has_references:
            raise HTTPConflict(
                detail="Urireferencer: The uri {0} is still in use by other applications: {1}".
                    format(uri, ', '.join([app.title for app in registery_response.applications])))
        return fn(parent_object, *args, **kw)

    return advice