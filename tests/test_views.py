# -*- coding: utf-8 -*-

import json
import unittest
import httpretty
from pyramid import testing
from pyramid_urireferencer import IReferencer, Referencer, _add_referencer, get_referencer
from pyramid_urireferencer.views import ReferencesPluginView
from pyramid_urireferencer.models import RegistryResponse

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_add_get_referencer(self):
        registry = self.config.registry
        registry.registerUtility("referencer_test", IReferencer)
        r = _add_referencer(registry)
        self.assertEqual(get_referencer(registry), r)

    def test_add_get_referencer_without_config(self):
        registry = self.config.registry
        self.assertRaises(KeyError, _add_referencer, registry)

    def test_add_referencer(self):
        self.config.registry.settings['urireferencer.registry_url'] = 'http://my.registry.org'
        self.config.registry.settings['urireferencer.referencer'] = 'test_views.TestReferencer'
        ref = _add_referencer(self.config.registry)
        self.assertIsInstance(ref, TestReferencer)

    def test_is_referenced(self):
        uri = 'http://id.erfgoed.net/foobar/2'
        url = 'http://localhost:6543'
        from pyramid_urireferencer.renderers import registry_adapter
        reg_response_success_ref1 = registry_adapter(RegistryResponse(uri, True, False, 0, []), {})

        referencer = TestReferencer(url)
        self.assertIsNone(referencer.references(uri))
        response = referencer.is_referenced(uri)
        self.assertIsInstance(response, RegistryResponse)
        self.assertEqual(response.success, False)

        httpretty.enable()  # enable HTTPretty so that it will monkey patch the socket module
        httpretty.register_uri(
            httpretty.GET,
            '{0}/references?{1}'.format(url, urlencode({'uri': uri})),
            body=json.dumps(reg_response_success_ref1),
            content_type="application/json"
        )

        response = referencer.is_referenced(uri)
        self.assertIsInstance(response, RegistryResponse)
        self.assertTrue(response.success)

        httpretty.disable()  # disable afterwards, so that you will have no problems in code that uses that socket module
        httpretty.reset()


class TestReferencer(Referencer):
    def references(self, uri):
        return None
