.PHONY: clean test tests all server

all: tests

clean:
	find -x . -name '*.py[co]' | xargs rm -rf
	find -x . -name '__pycache__' | xargs rm -rf
	find -x . -name '*.css' | xargs rm -rf
	rm -rf .tox
	rm -rf data
	rm MANIFEST

tests: test

test:
	tox -v -e test


coverage:
	tox -v -e cover

pep8:
	tox -v -e pep8

server:
	bash -c 'source .tox/test/bin/activate && python */app.py --debug'

data:
	mkdir -p data

data/bikes.json: data
	curl https://data.sfgov.org/api/views/w969-5mn4/rows.json?accessType=DOWNLOAD > data/bikes.json

data/films.json: data
	curl https://data.sfgov.org/api/views/yitu-d5am/rows.json?accessType=DOWNLOAD > data/films.json

data/foods.json: data
	curl https://data.sfgov.org/api/views/rqzj-sfat/rows.json?accessType=DOWNLOAD > data/foods.json

