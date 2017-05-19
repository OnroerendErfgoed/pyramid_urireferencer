# -*- coding: utf-8 -*-

from pyramid.view import view_config
from pyramid_urireferencer import get_referencer

import logging

log = logging.getLogger(__name__)


class ApplicatieView(object):
    def __init__(self, request):
        self.request = request


class RestView(ApplicatieView):
    pass


class ReferencesPluginView(RestView):
    @view_config(route_name='references', renderer='json_item', accept='application/json')
    def get_references(self):
        return get_referencer(self.request.registry).references(self.request.params.get('uri'), self.request)
