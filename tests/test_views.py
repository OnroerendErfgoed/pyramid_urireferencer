import json
import unittest
import httpretty
from pyramid import testing
from pyramid_urireferencer import IReferencer, Referencer, _add_referencer, get_referencer
from pyramid_urireferencer.views import ReferencesPluginView
from pyramid_urireferencer.models import RegistryResponse

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

    def test_add_get_referencer_error(self):
        registry = self.config.registry
        self.assertRaises(NotImplementedError, _add_referencer, registry)

    def test_is_referenced(self):
        uri = 'http://id.erfgoed.net/foobar/2'
        base_uri = 'http://id.erfgoed.net/foobar'
        url = 'http://localhost:6543'
        reg_response_success_ref1 = RegistryResponse(uri, base_uri, True, False, 0, []).__json__(None)

        referencer = TestReferencer(url)
        self.assertIsNone(referencer.references(uri))
        response = referencer.is_referenced(uri)
        self.assertIsInstance(response, RegistryResponse)
        self.assertEqual(response.success, False)

        httpretty.enable()  # enable HTTPretty so that it will monkey patch the socket module
        httpretty.register_uri(httpretty.GET, url + '/references?uri=' + uri,
                       body=json.dumps(reg_response_success_ref1),
                       content_type="application/json")

        response = referencer.is_referenced(uri)
        self.assertIsInstance(response, RegistryResponse)
        self.assertTrue(response.success)

        httpretty.disable()  # disable afterwards, so that you will have no problems in code that uses that socket module
        httpretty.reset()

    def test_get_references(self):
        self.assertRaises(NotImplementedError, ReferencesPluginView(testing.DummyRequest()).get_references)


class TestReferencer(Referencer):
    def references(self, uri):
        return None
