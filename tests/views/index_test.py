#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib


def test_index(app):
    response = app.get('/')
    assert response.status_code == httplib.OK, response.get_data()
