#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from app import get_application


@pytest.fixture
def app():
	app = get_application(debug=True).test_client()
	return app
