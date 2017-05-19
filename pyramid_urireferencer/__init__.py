# -*- coding: utf-8 -*-

from pyramid.path import (
    DottedNameResolver
)
from zope.interface import Interface

from .referencer import Referencer
from .renderers import json_renderer


class IReferencer(Interface):
    pass


def includeme(config):
    """this function adds some configuration for the application"""
    config.add_route('references', '/references')
    _add_referencer(config.registry)
    config.add_renderer('json_item', json_renderer)
    config.scan()


def _add_referencer(registry):
    """
    Gets the Referencer from config and adds it to the registry.
    """
    referencer = registry.queryUtility(IReferencer)
    if referencer is not None:
        return referencer
    ref = registry.settings['urireferencer.referencer']
    url = registry.settings['urireferencer.registry_url']
    r = DottedNameResolver()
    registry.registerUtility(r.resolve(ref)(url), IReferencer)
    return registry.queryUtility(IReferencer)


def get_referencer(registry):
    """
    Get the referencer class

    :rtype: pyramid_urireferencer.referencer.AbstractReferencer
    """
    # Argument might be a config or request
    regis = getattr(registry, 'registry', None)
    if regis is None:
        regis = registry
    return regis.queryUtility(IReferencer)
