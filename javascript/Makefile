BABEL = node_modules/.bin/babel

.PHONY: build clean dist

build:
	babel src/ --modules common --out-dir dist
	browserify --bare -r react ./index.js -o ./dist/template-server.js

clean:
	rm -rf dist

dist: clean build
	make clean
	make build