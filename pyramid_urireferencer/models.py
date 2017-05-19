# -*- coding: utf-8 -*-

import json


class RegistryResponse:
    """
    Represents what the registry will send back to a client when asked if
    a certain uri is used somewhere.

    :param string query_uri: Uri of the resource unser survey.
    :param boolean success: Were all the queries successful?
    :param boolean has_references: Were any references found?
    :param int count: How many references were found?
    :param list applications: A list of application results.
    """

    def __init__(self, query_uri, success, has_references, count, applications):
        self.query_uri = query_uri
        self.success = success
        self.has_references = has_references
        self.count = count
        self.applications = applications

    @staticmethod
    def load_from_json(data):
        """
        Load a :class:`RegistryReponse` from a dictionary or a string (that
        will be parsed as json).
        """
        if isinstance(data, str):
            data = json.loads(data)
        applications = [
            ApplicationResponse.load_from_json(a) for a in data['applications']
        ] if data['applications'] is not None else []
        return RegistryResponse(
            data['query_uri'], data['success'],
            data['has_references'], data['count'], applications
        )

    def to_json(self):
        return {
            "query_uri": self.query_uri,
            "success": self.success,
            "has_references": self.has_references,
            "count": self.count,
            "applications": [app.to_json() for app in self.applications]
        }


class ApplicationResponse:
    """
    Represents what a certain application will send back to the registry when
    asked if a certain uri is used by the application.

    :param string title: Title of the application
    :param string uri: A uri for the application, not guaranteed to be a http url.
    :param string service_url: The url that answered the question
    :param boolean success: Was the querie successful?
    :param boolean has_references: Were any references found?
    :param int count: How many references were found?
    :param list items: A list of items that have a reference to the \
        uri under survey. Limited to 5 items for performance reasons.
    """

    def __init__(self, title, uri, service_url, success, has_references, count, items):
        self.title = title
        self.uri = uri
        self.service_url = service_url
        self.success = success
        self.has_references = has_references
        self.count = count
        self.items = items

    @staticmethod
    def load_from_json(data):
        """
        Load a :class:`ApplicationResponse` from a dictionary or string (that
        will be parsed as json).
        """
        if isinstance(data, str):
            data = json.loads(data)
        items = [Item.load_from_json(a) for a in data['items']] if data['items'] is not None else []
        return ApplicationResponse(
            data['title'], data['uri'], data['service_url'],
            data['success'], data['has_references'], data['count'], items
        )

    def to_json(self):
        return {
            "title": self.title,
            "uri": self.uri,
            "service_url": self.service_url,
            "success": self.success,
            "has_references": self.has_references,
            "count": self.count,
            "items": [item.to_json() for item in self.items] if self.items else []
        }


class Item:
    """
    A single item that holds a reference to the queried uri.

    :param string title: Title of the item.
    :param string uri: Uri of the item.
    """

    def __init__(self, title, uri):
        self.title = title
        self.uri = uri

    @staticmethod
    def load_from_json(data):
        """
        Load a :class:`Item` from a dictionary ot string (that will be parsed
        as json)
        """
        if isinstance(data, str):
            data = json.loads(data)
        return Item(data['title'], data['uri'])

    def to_json(self):
        return {
            "title": self.title,
            "uri": self.uri
        }
