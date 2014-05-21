#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock
import pytest

from parkit.app import get_application


@pytest.fixture
def app():
    app = get_application(debug=True).test_client()
    return app


@pytest.yield_fixture(autouse=True)
def db_find():
    """Mock out mongo."""
    with mock.patch('parkit.db.find') as find:
        find.return_value = [{'type': 'bike', 'loc': 'foobar'}]
        yield find
