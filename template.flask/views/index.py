#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template


index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
	return render_template('index.html')


