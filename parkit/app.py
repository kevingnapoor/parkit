#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask
from flask.ext.assets import Bundle
from flask.ext.assets import Environment

from parkit.views import index
from parkit.views import search


def get_application(debug=False):
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static',
        static_url_path='',
    )

    app.debug = debug

    bundle_assets(app, minify=bool(not debug))

    register_routes(app)

    if os.getenv('API_KEY'):
        app.config['API_KEY'] = os.getenv('API_KEY')
    else:
        with open('api_key', 'r') as f:
            app.config['API_KEY'] = f.read()

    return app


def bundle_assets(app, minify=True):
    js_filters = ['yui_js'] if minify else None
    css_filters = ['yui_css'] if minify else None

    js = Bundle(
        'js/google_maps.js',
        'js/ajax.js',
        filters=js_filters,
        output='gen/packed.js',
    )
    css = Bundle(
        'css/style.css',
        'css/responsive.css',
        'css/fonts.css',
        filters=css_filters,
        output='gen/packed.css',
    )

    assets = Environment()
    assets.register('js', js)
    assets.register('css', css)

    app.config['ASSETS_DEBUG'] = not minify

    assets.init_app(app)


def register_routes(app):
    app.add_url_rule('/', 'index', index.get_index)
    app.add_url_rule('/index', 'index', index.get_index)
    app.add_url_rule('/search', 'search', search.get_search)


if __name__ == '__main__':
    arg = sys.argv[-1]
    debug = bool(arg == '--debug')

    if len(sys.argv) > 1 and not debug:
        print 'python app.py [--debug]'
        sys.exit(1)

    app = get_application(debug=debug)

    port = int(os.environ.get('PORT', 8080))

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_debugger=debug,
    )
