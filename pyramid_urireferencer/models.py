# -*- coding: utf-8 -*-

import json

class RegistryResponse:
    def __init__(self, uri, success, has_references, count, applications):
            self.uri = uri
            self.success = success
            self.has_references = has_references
            self.count = count
            self.applications = applications

    @staticmethod
    def load_from_json(data):
        r = RegistryResponse(None, None, None, None, None)
        if isinstance(data, str):
            data = json.loads(data)
        r.uri = data['query_uri']
        r.success = data['success']
        r.has_references = data['has_references']
        r.count = data['count']
        r.applications = [ApplicationResponse.load_from_json(a) for a in data['applications']] if data['applications'] is not None else None
        return r


class ApplicationResponse:
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
    def __init__(self, title, uri):
        self.title = title
        self.uri = uri

    @staticmethod
    def load_from_json(data):
        r = Item(None, None)
        if isinstance(data, str):
            data = json.loads(data)
        r.uri = data['uri']
        r.name = data['title']
        return r
