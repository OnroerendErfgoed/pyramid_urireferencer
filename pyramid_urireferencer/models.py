# -*- coding: utf-8 -*-

import json


class RegistryResponse:
    '''
    Represents what the registry will send back to a client when asked if
    a certain uri is used somewhere.
    '''
    def __init__(self, query_uri, success, has_references, count, applications):
            self.query_uri = query_uri
            self.success = success
            self.has_references = has_references
            self.count = count
            self.applications = applications

    @staticmethod
    def load_from_json(data):
        '''
        Load a :class:`RegistryReponse` from a dictionary or a string (that
        will be parsed as josn).
        '''
        r = RegistryResponse(None, None, None, None, None)
        if isinstance(data, str):
            data = json.loads(data)
        r.query_uri = data['query_uri']
        r.success = data['success']
        r.has_references = data['has_references']
        r.count = data['count']
        r.applications = [ApplicationResponse.load_from_json(a) for a in data['applications']] if data['applications'] is not None else None
        return r


class ApplicationResponse:
    '''
    Represents what a certain application will send back to the registry when
    asked if a certain uri is used by the application.
    '''
    def __init__(self, title, uri, url, success, has_references, count, items):
            self.title = title
            self.uri = uri
            self.url = url
            self.success = success
            self.has_references = has_references
            self.count = count
            self.items = items

    @staticmethod
    def load_from_json(data):
        r = ApplicationResponse(None, None, None, None, None, None, None)
        if isinstance(data, str):
            data = json.loads(data)
        r.name = data['title']
        r.uri = data['uri']
        r.url = data['url']
        r.success = data['success']
        r.has_references = data['has_references']
        r.count = data['count']
        r.items = [Item.load_from_json(a) for a in data['items']] if data['items'] is not None else None
        return r


class Item:
    '''
    A single item that holds a reference to the queried uri.
    '''
    def __init__(self, title, uri):
        self.title = title
        self.uri = uri

    @staticmethod
    def load_from_json(data):
        i = Item(None, None)
        if isinstance(data, str):
            data = json.loads(data)
        i.uri = data['uri']
        i.title = data['title']
        return i
