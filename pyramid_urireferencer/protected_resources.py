# -*- coding: utf-8 -*-
from pyramid.httpexceptions import (
    HTTPInternalServerError,
    HTTPConflict)

from pyramid_urireferencer import get_referencer

'''
Thid module is used when blocking operations on a certain uri
that might be used in external applications.
:versionadded: 0.4.0
'''



def protected_operation(fn):
    '''
    use this decorator to prevent an operation from being executed
    when the related uri resource is still in use
    '''

    def advice(parent_object, *args, **kw):
        id = parent_object.request.matchdict['id']
        referencer = get_referencer(parent_object.request.registry)
        registery_response = referencer.is_referenced(parent_object.uri_template.format(id))
        if not registery_response.success:
            raise HTTPInternalServerError(detail="Urireferencer: Er gaat iets mis bij het ophalen van de referenties")
        if registery_response.has_references:
            raise HTTPConflict(
                detail="Urireferencer: Er wordt gerefereerd naar het advies in de applicatie(s) {0}".
                    format(', '.join([app.title for app in registery_response.applications])))
        return fn(parent_object, *args, **kw)

    return advice