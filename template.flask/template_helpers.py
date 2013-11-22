#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import url_for
from flask import Markup


static_url = lambda x, *a, **kw: url_for('static', filename=x, *a, **kw)

css_url = lambda x, *a, **kw: static_url('css/' + x, *a, **kw)

def css(x, *a, **kw):
	return Markup(
		'<link rel=stylesheet type=text/css href="%s">' % css_url(x, *a, **kw),
	)

