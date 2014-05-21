#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock
import pytest

from parkit.app import get_application


@pytest.mark.parametrize('debug', [True, False])
def test_get_application(debug):
    app = get_application(debug=debug)
    assert app.config['API_KEY']


def test_get_application_with_api_key_in_env():
    with mock.patch.dict('os.environ', {'API_KEY': 'foo'}):
        app = get_application()
    assert app.config['API_KEY'] == 'foo'
