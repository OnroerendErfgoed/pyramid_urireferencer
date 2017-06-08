# -*- coding: utf-8 -*-

import abc
import six
import requests

import logging
from .models import RegistryResponse

log = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class AbstractReferencer:
    """
    This is an abstract class that defines what a Referencer needs to be able to handle.

    It does two things:
    
        * Check if a uri is being used in this application and report on this.
        * Check if a certain uri is being used in another application by query
          a central registry.
          * this requires a function :meth:`get_uri` to determine the uri of the current request
    """

    @abc.abstractmethod
    def get_uri(self, request):
        """
        This method extracts a uri from the request. This is the uri that needs to be checked.

        :param request: :class:`pyramid.request.Request` with useful configuration information and connections
                        of the application (registry, route_url, session) to determine the references
        :rtype: string uri: URI of the resource we need to check for
        """

    @abc.abstractmethod
    def references(self, uri, request):
        """
        This method checks if a certain uri is being referenced by any other
        resource within this application.

        :param string uri: URI of the resource we need to check for
        :param request: :class:`pyramid.request.Request` with useful configuration information and connections
                        of the application (registry, route_url, session) to determine the references
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


@six.add_metaclass(abc.ABCMeta)
class Referencer(AbstractReferencer):
    """
    This is an implementation of the :class:`AbstractReferencer` that adds a
    generic :meth:`is_referenced` method and plain methods: :meth:`references` and :meth:`get_uri` 
    """

    def __init__(self, registry_url, **kwargs):
        """
        :param string registry_url: Locatie where the central registry can be
            found
        """
        self.registry_url = registry_url

    def is_referenced(self, uri):
        """
        This method checks if a certain uri is being referenced from resources
        in other applications.

        :param string uri: URI of the resource that needs to be checked
        :rtype: :class:`pyramid_urireferencer.models.RegistryResponse`
        """
        try:
            url = '{0}/references'.format(self.registry_url)
            r = requests.get(url, params={'uri': uri})
            return RegistryResponse.load_from_json(r.json())
        except Exception as e:
            log.error(e)
            return RegistryResponse(uri, False, None, None, None)
