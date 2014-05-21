#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template


def get_index():
    return render_template('index.html')
