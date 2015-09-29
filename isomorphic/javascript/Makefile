BABEL = node_modules/.bin/babel

.PHONY: build clean dist

build:
	browserify --bare -r react ./index.js -o ./dist/template-server.js

clean:
	rm -rf dist

dist: clean build
	make clean
	make build
