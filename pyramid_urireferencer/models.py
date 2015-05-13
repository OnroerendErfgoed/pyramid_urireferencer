import json

class RegistryResponse:
    def __init__(self, uri, base_uri, success, has_references, count, applications):
            self.uri = uri
            self.base_uri = base_uri
            self.success = success
            self.has_references = has_references
            self.count = count
            self.applications = applications
    def __json__(self, request):
        return {
            'request': {'uri': self.uri},
            'response':
                {
                    'success': self.success,
                    'has_references': self.has_references,
                    'base_uri': self.base_uri,
                    'count': self.count,
                    'applications': self.applications
                }
        }

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @staticmethod
    def load_from_json(data):
        try:
            r = RegistryResponse(None, None, None, None, None, None)
            if isinstance(data, str):
                data = json.loads(data)
            response = data['response']
            r.uri = data['request']['uri']
            r.base_uri = response['base_uri']
            r.success = response['success']
            r.has_references = response['has_references']
            r.count = response['count']
            r.applications = [ApplicationResponse.load_from_json(a) for a in response['applications']] if response['applications'] is not None else None
            return r
        except:
            raise ValueError("json kan niet worden omgezet naar een geldig object")


class ApplicationResponse:
    def __init__(self, name, uri, url, success, has_references, count, items):
            self.name = name
            self.uri = uri
            self.url = url
            self.success = success
            self.has_references = has_references
            self.count = count
            self.items = items

    def __json__(self, request):
        return {
            'name': self.name,
            'uri': self.uri,
            'url': self.url,
            'success': self.success,
            'has_references': self.has_references,
            'count': self.count,
            'items': self.items
        }
    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @staticmethod
    def load_from_json(data):
        try:
            r = ApplicationResponse(None, None, None, None, None, None, None)
            if isinstance(data, str):
                data = json.loads(data)
            r.name = data['name']
            r.uri = data['uri']
            r.url = data['url']
            r.success = data['success']
            r.has_references = data['has_references']
            r.count = data['count']
            r.items = [Item.load_from_json(a) for a in data['items']] if data['items'] is not None else None
            return r
        except:
            raise ValueError("json kan niet worden omgezet naar een geldig object")

class Item:
    def __init__(self, name, uri):
        self.name = name
        self.uri = uri

    def __json__(self, request):
        return {
            'name': self.name,
            'uri': self.uri
        }

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @staticmethod
    def load_from_json(data):
        try:
            r = Item(None, None)
            if isinstance(data, str):
                data = json.loads(data)
            r.uri = data['uri']
            r.name = data['name']
            return r
        except:
            raise ValueError("json kan niet worden omgezet naar een geldig object")
