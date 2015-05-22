# -*- coding: utf-8 -*-

from pyramid_urireferencer.models import (
    RegistryResponse,
    ApplicationResponse,
    Item
)

class TestRenderers:

    def test_empty_registry_renderer(self):
        rr = RegistryResponse('http://id.example.org/foo/1', True, False, 0, [])
        from pyramid_urireferencer.renderers import registry_adapter
        r = registry_adapter(rr, {})
        assert r['query_uri'] == 'http://id.example.org/foo/1'
        assert r['success']
        assert not r['has_references']
        assert r['count'] == 0
        assert len(r['applications']) == 0

    def test_registry_renderer_one_app_no_results(self):
        ar = ApplicationResponse(
            'My app',
            'http://something.example.org',
            'http://somethingelse.example.org',
            True,
            False,
            0,
            []
        )
        rr = RegistryResponse('http://id.example.org/foo/1', True, False, 0, [ar])
        from pyramid_urireferencer.renderers import registry_adapter
        r = registry_adapter(rr, {})
        assert r['query_uri'] == 'http://id.example.org/foo/1'
        assert r['success']
        assert not r['has_references']
        assert r['count'] == 0
        assert len(r['applications']) == 1
        assert 'title' in r['applications'][0]

    def test_empty_application_renderer(self):
        ar = ApplicationResponse(
            'My app',
            'http://something.example.org',
            'http://somethingelse.example.org/references',
            True,
            False,
            0,
            []
        )
        from pyramid_urireferencer.renderers import application_adapter
        r = application_adapter(ar, {})
        assert r['uri'] == 'http://something.example.org'
        assert r['service_url'] == 'http://somethingelse.example.org/references'
        assert r['success']
        assert not r['has_references']
        assert r['count'] == 0
        assert len(r['items']) == 0

    def test_application_renderer_one_item(self):
        ar = ApplicationResponse(
            'My app',
            'http://something.example.org',
            'http://somethingelse.example.org/references',
            True,
            False,
            0,
            [Item('http://something.example.org/thingy/thing', 'My item')]
        )
        from pyramid_urireferencer.renderers import application_adapter
        r = application_adapter(ar, {})
        assert r['uri'] == 'http://something.example.org'
        assert r['service_url'] == 'http://somethingelse.example.org/references'
        assert r['success']
        assert not r['has_references']
        assert r['count'] == 0
        assert len(r['items']) == 1
        assert 'title' in r['items'][0]
        assert 'uri' in r['items'][0]

