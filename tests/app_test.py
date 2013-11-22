#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock

from app import get_application


class TestApp(object):

	def test_generate_css(self):
		with mock.patch('scss.Scss') as Scss:
			get_application(generate_css=True)
		assert Scss.called

	def test_dont_generate_css(self):
		with mock.patch('scss.Scss') as Scss:
			get_application(generate_css=False)
		assert not Scss.called


