from pyramid.config import Configurator
from pyramid.path import (
    DottedNameResolver
)
from zope.interface import Interface
from .referencer import Referencer

class IReferencer(Interface):
    pass

registry_url=None

def includeme(config):
    """this function adds some configuration for the application"""
    # config.include('pyramid_tm')
    # config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('references', '/references')
    _add_referencer(config.registry)
    # config.add_directive('referencer', referencer)
    config.scan('referencesplugin')

def _add_referencer(registry):
    """
    Gets the Referencer from config and adds it to the registry.
    """
    referencer = registry.queryUtility(IReferencer)
    if referencer is not None:
        return referencer
    try:
        ref = registry.settings['restregistry.referencer']
        url = registry.settings['restregistry.registry_url']
        r = DottedNameResolver()
        registry.registerUtility(r.resolve(ref)(url), IReferencer)
        return registry.queryUtility(IReferencer)
    except KeyError:
        raise NotImplementedError("De Referencer-class kon niet worden opgehaald.")

def get_referencer(registry):
    """
    Get the referencer class
    """
    #Argument might be a config or request
    regis = getattr(registry, 'registry', None)
    if regis is None:
        regis = registry
    return regis.queryUtility(IReferencer)
