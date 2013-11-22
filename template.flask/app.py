#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask
from flask.ext import scss

from garbage import GarbageCollector
from template_helpers import css


def get_application(generate_css=True, debug=False):
	app = Flask(__name__,
			template_folder='templates',
			static_folder='static',
			static_url_path='',
	)

	from views.index import index_bp
	app.register_blueprint(index_bp)

	if generate_css:
		# force debug because we don't deploy css
		app.debug = True
		app_dir = os.path.dirname(app.static_folder)
		scss.Scss(app,
				static_dir=app.static_folder,
				asset_dir=os.path.join(app_dir, 'assets')
		)

	app.debug = debug

	@app.context_processor
	def context_globals():
		return dict(
			css=css,
		)

	return app


if __name__ == '__main__':
	arg = sys.argv[-1]
	debug = bool(arg == '--debug')

	if len(sys.argv) > 1 and not debug:
		print 'python app.py [--debug]'
		sys.exit(1)

	app = get_application(debug=debug)

	port = int(os.environ.get('PORT', 8080))

	with GarbageCollector().gc_disabled():
		app.run(
				host='0.0.0.0',
				port=port,
				debug=debug,
				use_debugger=debug,
		)

