# -*- coding: utf-8 -*-

import abc
import requests

import logging
log = logging.getLogger(__name__)

from .models import RegistryResponse

class AbstractReferencer:
    """
    This is an abstract class that defines what a Referencer needs to be able to handle.

    It does two things:

        * Check if a uri is being used in this application and report on this.
        * Check if a certain uri is being used in another application by query
          a central registry.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def references(self, uri):
        """
        This method checks if a certain uri is being referenced by any other
        resource within this application.

        :param string uri: URI of the resource we need to check for
        :rtype: :class:`pyramid_urireferencer.models.ApplicationResponse`
        """

    @abc.abstractmethod
    def is_referenced(self, uri):
        """
        This method checks if a certain uri is being referenced from resources
        in other applications.

        :param string uri: URI of the resource that needs to be checked
        :rtype: :class:`pyramid_urireferencer.models.RegistryResponse`
        """


class Referencer(AbstractReferencer):
    """
    This is an implementation of the :class:`AbstractReferencer` that adds a
    generic :meth:`is_referenced` method and a plain :meth:`references` method..
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, registry_url, **kwargs):
        '''
        :param string registry_url: Locatie where the central registry can be
            found
        '''
        self.registry_url = registry_url

    def is_referenced(self, uri):
        """
        This method checks if a certain uri is being referenced from resources
        in other applications.

        :param string uri: URI of the resource that needs to be checked
        :rtype: :class:`pyramid_urireferencer.models.RegistryResponse`
        """
        try:
            url = self.registry_url + '/references?uri=' + uri
            r = requests.get(url)
            return RegistryResponse.load_from_json(r.json())
        except Exception as e:
            log.error(e)
            return RegistryResponse(uri, False, None, None, None)
