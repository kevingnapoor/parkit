#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib


class TestIndexIntegration(object):

	def test_index(self, app):
		response = app.get('/')
		assert response.status_code == httplib.OK, response.get_data()
