# -*- coding: utf-8 -*-
import logging
import unittest

import pytest
from pyramid import testing
from webob.acceptparse import AcceptValidHeader

from pyramid_urireferencer.protected_resources import protected_operation
from pyramid_urireferencer.protected_resources \
    import protected_operation_with_request
from pyramid_urireferencer.models import RegistryResponse, Item, ApplicationResponse
from pyramid.httpexceptions import HTTPConflict, HTTPInternalServerError

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch  # pragma: no cover


def get_app(nr):
    items = []
    if nr == 1:
        items.append(Item(uri="https://dev-besluiten.onroerenderfgoed.be/besluiten/152", title="Mijn besluit"))
        items.append(Item(uri="https://dev-besluiten.onroerenderfgoed.be/besluiten/154",
                          title="Vaststelling van de inventaris van het Bouwkundig Erfgoed op 28 november 2014"))
    a = ApplicationResponse(
            title='App {0}'.format(nr),
            uri="https://dev-app-{0}.onroerenderfgoed.be/".format(nr),
            service_url="https://dev-app-{0}.onroerenderfgoed.be/references".format(nr),
            success=True,
            has_references=True if nr == 1 else False,
            count=2 if nr == 1 else 0,
            items=items
    )
    return a


def get_app_500():
    return ApplicationResponse(
        title='App',
        uri="https://dev-app.onroerenderfgoed.be/",
        service_url="https://dev-app.onroerenderfgoed.be/references",
        success=False,
        has_references=None,
        count=None,
        items=None
    )


class DummyParent(object):
    def __init__(self, accepts='*/*'):
        self.request = testing.DummyRequest()
        self.request.accept = AcceptValidHeader(accepts)
        config = testing.setUp(request=self.request)
        config.registry.settings = {
            'urireferencer.referencer': 'test_views.TestReferencer',
            'urireferencer.registry_url': 'http://my.registry.org'
        }
        config.include('pyramid_urireferencer')

    @protected_operation
    def protected_dummy(self):
        return 'dummy ok'


class ProtectedTests(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.WARN)

    @patch('pyramid_urireferencer.protected_resources.pyramid_urireferencer.Referencer.is_referenced')
    def test_protected_operation(self, is_referenced_mock):
        dummy = DummyParent('application/html')
        is_referenced_mock.return_value = RegistryResponse('https://id.erfgoed.net/resources/1', True, False, 0, [])
        dummy.protected_dummy()
        is_referenced_call = is_referenced_mock.mock_calls[0]
        self.assertEqual('https://id.erfgoed.net/resources/1', is_referenced_call[1][0])

    @patch('pyramid_urireferencer.protected_resources.pyramid_urireferencer.Referencer.is_referenced')
    def test_protected_operation_409(self, is_referenced_mock):
        dummy = DummyParent(accepts='application/html')
        is_referenced_mock.return_value = RegistryResponse('https://id.erfgoed.net/resources/1', True, True, 10,
                                                           [get_app(1), get_app(2)])
        self.assertRaises(HTTPConflict, dummy.protected_dummy)
        is_referenced_call = is_referenced_mock.mock_calls[0]
        self.assertEqual('https://id.erfgoed.net/resources/1', is_referenced_call[1][0])

    @patch('pyramid_urireferencer.protected_resources.pyramid_urireferencer.Referencer.is_referenced')
    def test_protected_operation_409_2(self, is_referenced_mock):
        dummy = DummyParent(accepts='application/html')
        is_referenced_mock.return_value = RegistryResponse('https://id.erfgoed.net/resources/1', False, True, 10,
                                                           [get_app(1), get_app(2)])
        self.assertRaises(HTTPConflict, dummy.protected_dummy)
        is_referenced_call = is_referenced_mock.mock_calls[0]
        self.assertEqual('https://id.erfgoed.net/resources/1', is_referenced_call[1][0])

    @patch('pyramid_urireferencer.protected_resources.pyramid_urireferencer.Referencer.is_referenced')
    def test_protected_operation_409_json(self, is_referenced_mock):
        dummy = DummyParent('application/json')
        is_referenced_mock.return_value = RegistryResponse('https://id.erfgoed.net/resources/1', False, True, 2,
                                                           [get_app(1), get_app(2)])
        res = dummy.protected_dummy()
        self.assertEqual(409, res.status_code)
        self.assertEqual(res.json_body["message"],
                         "The uri https://id.erfgoed.net/resources/1 is still in use by other applications. A total of 2 references have been found.")
        self.assertEqual("application/json", res.content_type)

        is_referenced_call = is_referenced_mock.mock_calls[0]
        self.assertEqual('https://id.erfgoed.net/resources/1', is_referenced_call[1][0])

    @patch('pyramid_urireferencer.protected_resources.pyramid_urireferencer.Referencer.is_referenced')
    def test_protected_operation_409_json_multiple(self, is_referenced_mock):
        dummy = DummyParent('application/json, application/html')
        is_referenced_mock.return_value = RegistryResponse(
            'https://id.erfgoed.net/resources/1', False, True, 2,
            [get_app(1), get_app(2)])
        res = dummy.protected_dummy()
        self.assertEqual(409, res.status_code)
        self.assertEqual(res.json_body["message"],
                         "The uri https://id.erfgoed.net/resources/1 is still in use by other applications. A total of 2 references have been found.")
        self.assertEqual("application/json", res.content_type)

        is_referenced_call = is_referenced_mock.mock_calls[0]
        self.assertEqual('https://id.erfgoed.net/resources/1', is_referenced_call[1][0])

    @patch('pyramid_urireferencer.protected_resources.pyramid_urireferencer.Referencer.is_referenced')
    def test_protected_operation_500(self, is_referenced_mock):
        dummy = DummyParent('application/html')
        is_referenced_mock.return_value = RegistryResponse('https://id.erfgoed.net/resources/1', False, None, None,
                                                           [get_app_500()])
        self.assertRaises(HTTPInternalServerError, dummy.protected_dummy)
        is_referenced_call = is_referenced_mock.mock_calls[0]
        self.assertEqual('https://id.erfgoed.net/resources/1', is_referenced_call[1][0])

    @patch('pyramid_urireferencer.protected_resources.pyramid_urireferencer.Referencer.is_referenced')
    def test_protected_operation_500_json(self, is_referenced_mock):
        dummy = DummyParent('application/json')
        is_referenced_mock.return_value = RegistryResponse('https://id.erfgoed.net/resources/1', False, None, None,
                                                           [get_app_500()])
        res = dummy.protected_dummy()
        self.assertEqual(500, res.status_code)
        self.assertEqual(res.json_body["message"],
                         "Unable to verify the uri https://id.erfgoed.net/resources/1 is no longer being used.")
        self.assertListEqual(res.json_body["errors"],
                             ["https://dev-app.onroerenderfgoed.be/: Could not verify the uri is no longer being used."])
        self.assertEqual("application/json", res.content_type)

        is_referenced_call = is_referenced_mock.mock_calls[0]
        self.assertEqual('https://id.erfgoed.net/resources/1', is_referenced_call[1][0])


@protected_operation_with_request
def protected_dummy(request):
    return 'dummy ok'


@patch('pyramid_urireferencer.protected_resources.pyramid_urireferencer'
       '.Referencer.is_referenced')
class TestProtectedWithRequest(object):
    def setUp(self):
        logging.basicConfig(level=logging.WARN)

    @pytest.fixture()
    def request(self):
        request = testing.DummyRequest()
        request.accept = AcceptValidHeader('application/html')
        config = testing.setUp(request=request)
        config.registry.settings = {
            'urireferencer.referencer': 'test_views.TestReferencer',
            'urireferencer.registry_url': 'http://my.registry.org'
        }
        config.include('pyramid_urireferencer')
        return request

    def test_protected_operation(self, is_referenced_mock, request):
        is_referenced_mock.return_value = RegistryResponse(
            'https://id.erfgoed.net/resources/1', True, False, 0, [])
        protected_dummy(request)
        is_referenced_call = is_referenced_mock.mock_calls[0]
        assert 'https://id.erfgoed.net/resources/1' == is_referenced_call[1][0]

    def test_protected_operation_409(self, is_referenced_mock, request):
        is_referenced_mock.return_value = RegistryResponse(
            'https://id.erfgoed.net/resources/1', True, True, 10,
            [get_app(1), get_app(2)])
        with pytest.raises(HTTPConflict):
            protected_dummy(request)
        is_referenced_call = is_referenced_mock.mock_calls[0]
        assert 'https://id.erfgoed.net/resources/1' == is_referenced_call[1][0]

    def test_protected_operation_409_2(self, is_referenced_mock, request):
        is_referenced_mock.return_value = RegistryResponse(
            'https://id.erfgoed.net/resources/1', False, True, 10,
            [get_app(1), get_app(2)])
        with pytest.raises(HTTPConflict):
            protected_dummy(request)
        is_referenced_call = is_referenced_mock.mock_calls[0]
        assert 'https://id.erfgoed.net/resources/1' == is_referenced_call[1][0]

    def test_protected_operation_409_json(self, is_referenced_mock, request):
        request.accept = AcceptValidHeader('application/json')
        is_referenced_mock.return_value = RegistryResponse(
            'https://id.erfgoed.net/resources/1', False, True, 2,
            [get_app(1), get_app(2)])
        res = protected_dummy(request)
        assert 409 == res.status_code
        msg = ("The uri https://id.erfgoed.net/resources/1 is still in use by "
               "other applications. A total of 2 references have been found.")
        assert res.json_body["message"] == msg
        assert "application/json" == res.content_type

        is_referenced_call = is_referenced_mock.mock_calls[0]
        assert 'https://id.erfgoed.net/resources/1' == is_referenced_call[1][0]

    def test_protected_operation_500(self, is_referenced_mock, request):
        is_referenced_mock.return_value = RegistryResponse(
            'https://id.erfgoed.net/resources/1', False, None, None,
            [get_app_500()])
        with pytest.raises(HTTPInternalServerError):
            protected_dummy(request)
        is_referenced_call = is_referenced_mock.mock_calls[0]
        assert 'https://id.erfgoed.net/resources/1' == is_referenced_call[1][0]

    def test_protected_operation_500_json(self, is_referenced_mock, request):
        request.accept = AcceptValidHeader('application/json')
        is_referenced_mock.return_value = RegistryResponse(
            'https://id.erfgoed.net/resources/1', False, None, None,
            [get_app_500()])
        res = protected_dummy(request)
        assert 500 == res.status_code
        msg = ("Unable to verify the uri https://id.erfgoed.net/resources/1 "
               "is no longer being used.")
        assert res.json_body["message"] == msg
        errors = ["https://dev-app.onroerenderfgoed.be/: Could not verify the "
                  "uri is no longer being used."]
        assert res.json_body["errors"] == errors
        assert "application/json" == res.content_type
        is_referenced_call = is_referenced_mock.mock_calls[0]
        assert 'https://id.erfgoed.net/resources/1' == is_referenced_call[1][0]
