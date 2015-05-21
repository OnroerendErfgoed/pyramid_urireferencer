# -*- coding: utf-8 -*-

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
                    'http://zotskap.be',
                    True,
                    True,
                    1,
                    [Item('Red with dots.', 'http://zotskapp.be/redwithdots')]
                )
            ]
        )
        assert rr.uri == 'http://id.example.org/me'
        assert rr.success
        assert rr.has_references
        assert rr.count == 1
        assert len(rr.applications) == 1


class TestApplicationResponse:

    def test_init(self):
        ar = ApplicationResponse(
            'Zotskapp',
            'http://zotskapp.be',
            'http://zotskapp.be',
            True,
            True,
            1,
            [Item('Red with dots.', 'http://zotskapp.be/redwithdots')]
        )
        assert ar.uri == 'http://zotskapp.be'
        assert ar.url == 'http://zotskapp.be'
        assert ar.success
        assert ar.has_references
        assert ar.count == 1
        assert len(ar.items) == 1
