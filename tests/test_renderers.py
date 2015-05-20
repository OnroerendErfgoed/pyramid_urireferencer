# -*- coding: utf-8 -*-

from pyramid_urireferencer.models import (
    RegistryResponse,
    ApplicationResponse
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

    def test_empty_application_renderer(self):
        ar = ApplicationResponse(
            'My app',
            'http://something.example.org', 
            'http://somethingelse.example.org',
            True,
            False,
            0,
            []
        )
        from pyramid_urireferencer.renderers import application_adapter
        r = application_adapter(ar, {})
        assert r['uri'] == 'http://something.example.org'
        assert r['url'] == 'http://somethingelse.example.org'
        assert r['success']
        assert not r['has_references']
        assert r['count'] == 0
        assert len(r['items']) == 0
