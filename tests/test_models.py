# -*- coding: utf-8 -*-

import json

from pyramid_urireferencer.models import (
    RegistryResponse,
    ApplicationResponse,
    Item
)

class TestRegistryResponse:

    def test_init(self):
        rr = RegistryResponse(
            'http://id.example.org/me',
            True,
            True,
            1,
            [
                ApplicationResponse(
                    'Zotskapp',
                    'http://zotskapp.be/',
                    'http://zotskap.be/references',
                    True,
                    True,
                    1,
                    [Item('Red with dots.', 'http://zotskapp.be/redwithdots')]
                )
            ]
        )
        assert rr.query_uri == 'http://id.example.org/me'
        assert rr.success
        assert rr.has_references
        assert rr.count == 1
        assert len(rr.applications) == 1

    def test_load_from_json(self):
        data = {
            'query_uri': 'http://id.example.org/me',
            'success': True,
            'has_references': False,
            'count': 0,
            'applications': []
        }
        rr = RegistryResponse.load_from_json(data)
        assert rr.query_uri == 'http://id.example.org/me'
        assert rr.success
        assert not rr.has_references
        assert rr.count == 0
        assert len(rr.applications) == 0

    def test_load_from_json_string(self):
        data = {
            'query_uri': 'http://id.example.org/me',
            'success': True,
            'has_references': False,
            'count': 0,
            'applications': []
        }
        data = json.dumps(data)
        rr = RegistryResponse.load_from_json(data)
        assert rr.query_uri == 'http://id.example.org/me'
        assert rr.success
        assert not rr.has_references
        assert rr.count == 0
        assert len(rr.applications) == 0

    def test_load_from_json_string_applications_none(self):
        data = {
            'query_uri': 'http://id.example.org/me',
            'success': True,
            'has_references': False,
            'count': 0,
            'applications': None
        }
        data = json.dumps(data)
        rr = RegistryResponse.load_from_json(data)
        assert rr.query_uri == 'http://id.example.org/me'
        assert rr.success
        assert not rr.has_references
        assert rr.count == 0
        assert len(rr.applications) == 0


class TestApplicationResponse:

    def test_init(self):
        ar = ApplicationResponse(
            'Zotskapp',
            'http://zotskapp.be',
            'http://zotskapp.be/references',
            True,
            True,
            1,
            [Item('Red with dots.', 'http://zotskapp.be/redwithdots')]
        )
        assert ar.uri == 'http://zotskapp.be'
        assert ar.service_url == 'http://zotskapp.be/references'
        assert ar.success
        assert ar.has_references
        assert ar.count == 1
        assert len(ar.items) == 1

    def test_load_from_json(self):
        data = {
            'title': 'Zotskapp',
            'uri': 'http://zotskapp.be',
            'service_url': 'http://zotskapp.be/references',
            'success': True,
            'has_references': True,
            'count': 1,
            'items': [{
                'uri': 'http://zotskapp.be/redwithdots',
                'title': 'Red with dots.'
            }]
        }
        ar = ApplicationResponse.load_from_json(data)
        assert isinstance(ar, ApplicationResponse)
        assert ar.uri == 'http://zotskapp.be'
        assert ar.service_url == 'http://zotskapp.be/references'
        assert ar.success
        assert ar.has_references
        assert ar.count == 1
        assert len(ar.items) == 1

    def test_load_from_json_string(self):
        data = {
            'title': 'Zotskapp',
            'uri': 'http://zotskapp.be',
            'service_url': 'http://zotskapp.be/references',
            'success': True,
            'has_references': True,
            'count': 1,
            'items': [{
                'uri': 'http://zotskapp.be/redwithdots',
                'title': 'Red with dots.'
            }]
        }
        data = json.dumps(data)
        ar = ApplicationResponse.load_from_json(data)
        assert isinstance(ar, ApplicationResponse)
        assert ar.uri == 'http://zotskapp.be'
        assert ar.service_url == 'http://zotskapp.be/references'
        assert ar.success
        assert ar.has_references
        assert ar.count == 1
        assert len(ar.items) == 1

    def test_load_from_json_string_no_items(self):
        data = {
            'title': 'Zotskapp',
            'uri': 'http://zotskapp.be',
            'service_url': 'http://zotskapp.be/references',
            'success': True,
            'has_references': False,
            'count': 0,
            'items': []
        }
        data = json.dumps(data)
        ar = ApplicationResponse.load_from_json(data)
        assert isinstance(ar, ApplicationResponse)
        assert ar.uri == 'http://zotskapp.be'
        assert ar.service_url == 'http://zotskapp.be/references'
        assert ar.success
        assert not ar.has_references
        assert ar.count == 0
        assert len(ar.items) == 0

class TestItem:

    def test_init(self):
        i = Item('Red with dots.', 'http://zotskapp.be/redwithdots')
        assert i.title == 'Red with dots.'
        assert i.uri == 'http://zotskapp.be/redwithdots'

    def test_load_from_json(self):
        data = {
            'uri': 'http://zotskapp.be/redwithdots',
            'title': 'Red with dots.'
        }
        i = Item.load_from_json(data)
        assert isinstance(i, Item)
        assert i.title == 'Red with dots.'
        assert i.uri == 'http://zotskapp.be/redwithdots'

    def test_load_from_json_string(self):
        data = {
            'uri': 'http://zotskapp.be/redwithdots',
            'title': 'Red with dots.'
        }
        data = json.dumps(data)
        i = Item.load_from_json(data)
        assert isinstance(i, Item)
        assert i.title == 'Red with dots.'
        assert i.uri == 'http://zotskapp.be/redwithdots'
