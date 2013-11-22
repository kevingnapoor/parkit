APPNAME=$(shell basename `pwd`)

.PHONY: clean dependencies env test tests all update

all: env

clean:
	find -x . -name '*.py[co]' | xargs rm -rf
	find -x . -name '__pycache__' | xargs rm -rf
	find -x . -name '*.css' | xargs rm -rf

tests: test

test:
	# avoid __pycache__ directories if we can
	PYTHONDONTWRITEBYTECODE=1 py.test -v --capture=no

coverage: test
	coverage run `which py.test` -v --capture=no
	coverage report -m --omit='*/.env/*'

env: dependencies

.env: requirements.txt
	virtualenv .env

dependencies: .env
	. .env/bin/activate
	.env/bin/pip install -r requirements.txt

update: .env
	. .env/bin/activate
	.env/bin/pip install -rU requirements.txt

flakes:
	find . -name '*.py' -not -path '*.env*' | xargs pyflakes

server:
	PYTHONPATH=$(APPNAME) python $(APPNAME)/app.py --debug

