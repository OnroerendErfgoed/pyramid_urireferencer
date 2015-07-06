# -*- coding: utf-8 -*-
import unittest
from pyramid import testing
from pyramid_urireferencer.protected_resources import protected_operation
from pyramid_urireferencer.models import RegistryResponse
from pyramid.httpexceptions import HTTPConflict, HTTPInternalServerError
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch  # pragma: no cover

def get_app(nr):
    class Object(object):
        pass
    a = Object()
    a.title = 'App {0}'.format(nr)
    a.has_references = True if nr == 1 else False
    return a

class DummyParent(object):

    def __init__(self):
        self.request = testing.DummyRequest()
        config = testing.setUp(request=self.request)
        config.registry.settings = {
            'urireferencer.referencer': 'test_views.TestReferencer',
            'urireferencer.registry_url': 'http://my.registry.org'
        }
        config.include('pyramid_urireferencer')

        self.request.matchdict = {'id': 1}
        self.uri_template = 'https://id.erfgoed.net/resources/{0}'

    @protected_operation
    def protected_dummy(self):
        return 'dummy ok'


class ProtectedTests(unittest.TestCase):

    def setUp(self):
        pass

    @patch('pyramid_urireferencer.protected_resources.pyramid_urireferencer.Referencer.is_referenced')
    def test_protected_operation(self, is_referenced_mock):
        dummy = DummyParent()
        is_referenced_mock.return_value = RegistryResponse('https://id.erfgoed.net/resources/1', True, False, 0, [])
        dummy.protected_dummy()
        is_referenced_call = is_referenced_mock.mock_calls[0]
        self.assertEqual('https://id.erfgoed.net/resources/1', is_referenced_call[1][0])

    @patch('pyramid_urireferencer.protected_resources.pyramid_urireferencer.Referencer.is_referenced')
    def test_protected_operation_409(self, is_referenced_mock):
        dummy = DummyParent()
        is_referenced_mock.return_value = RegistryResponse('https://id.erfgoed.net/resources/1', True, True, 10, [get_app(1), get_app(2)])
        self.assertRaises(HTTPConflict, dummy.protected_dummy)
        is_referenced_call = is_referenced_mock.mock_calls[0]
        self.assertEqual('https://id.erfgoed.net/resources/1', is_referenced_call[1][0])

    @patch('pyramid_urireferencer.protected_resources.pyramid_urireferencer.Referencer.is_referenced')
    def test_protected_operation_409_2(self, is_referenced_mock):
        dummy = DummyParent()
        is_referenced_mock.return_value = RegistryResponse('https://id.erfgoed.net/resources/1', False, True, 10, [get_app(1), get_app(2)])
        self.assertRaises(HTTPConflict, dummy.protected_dummy)
        is_referenced_call = is_referenced_mock.mock_calls[0]
        self.assertEqual('https://id.erfgoed.net/resources/1', is_referenced_call[1][0])

    @patch('pyramid_urireferencer.protected_resources.pyramid_urireferencer.Referencer.is_referenced')
    def test_protected_operation_500(self, is_referenced_mock):
        dummy = DummyParent()
        is_referenced_mock.return_value = RegistryResponse('https://id.erfgoed.net/resources/1', False, None, None, None)
        self.assertRaises(HTTPInternalServerError, dummy.protected_dummy)
        is_referenced_call = is_referenced_mock.mock_calls[0]
        self.assertEqual('https://id.erfgoed.net/resources/1', is_referenced_call[1][0])

