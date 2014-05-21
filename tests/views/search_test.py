#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib

import pytest


def search_url(lat=37.7860099, lng=-122.4025387, type="bike"):
    url = '/search?'
    if lat:
        url += 'lat=%s&' % lat
    if lng:
        url += 'lng=%s&' % lng
    if type:
        url += 'type=%s&' % type
    return url


@pytest.mark.parametrize('type', ['bike', 'film', 'food'])
def test_valid_search(app, type):
    response = app.get(search_url(type=type))
    body = response.get_data()
    assert response.status_code == httplib.OK
    assert 'foobar' in body


def test_valid_search_using_defaults(app, db_find):
    response = app.get(search_url(None, None, None))
    body = response.get_data()
    assert response.status_code == httplib.OK
    assert 'foobar' in body
    db_find.assert_called_once_with(
        lat=37.7860099, lng=-122.4025387, type="bike"
    )


@pytest.mark.parametrize('lat, lng, type', [
    (37, 'A', 'bike'),
    (37, -190, 'bike'),
    (-100, -122, 'bike'),
    ('B', -122, 'bike'),
    (37, -122, 'lyft'),
])
def test_search_with_bad_params(app, lat, lng, type):
    response = app.get(search_url(lat=lat, lng=lng, type=type))
    body = response.get_data()
    assert response.status_code == httplib.BAD_REQUEST
    assert 'foobar' not in body
