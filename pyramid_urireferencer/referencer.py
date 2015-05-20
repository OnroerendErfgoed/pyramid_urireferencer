# -*- coding: utf-8 -*-

import abc
import requests

import logging
log = logging.getLogger(__name__)

from .models import RegistryResponse


class Referencer:
    """
    Interface voor de referencesPlugin. De plugin staat in voor volgende zaken:
    1) Nagaan of een uri uit een authentieke bron gebruikt wordt in de applicatie die de plugin inplugt.
    2) Controleren of een uri uit de eigen applicatie gebruikt wordt in een andere applicatie door middel van het raadplegen van de registry.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, registry_url, **kwargs):
        '''Create a new referencer-object
        '''
        self.registry_url = registry_url

    @abc.abstractmethod
    def references(self, uri):
        """
        Abstract method (to implement by the application that implements the plugin) to check if a specific uri is used in the application
        :param: :class: String unique resource identifier (uri)
        :rtype: :class: ApplicationResponse
        """

    def is_referenced(self, uri):
        """
        Method that the application can use to check if there are other applications known in the central registry that reference to the specific uri
        :param: :class: String unique resource identifier (uri)
        :rtype: :class: Response returns information about the applications that reference to the specific uri
        """
        try:
            url = self.registry_url + '/references?uri=' + uri
            r = requests.get(url)
            return RegistryResponse.load_from_json(r.json())
        except Exception as e:
            log.error(e)
            return RegistryResponse(uri, False, None, None, None)


