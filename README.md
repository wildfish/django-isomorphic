# Django JavaScript template engine

![https://travis-ci.org/wildfish/django-isomorphic.svg](https://travis-ci.org/wildfish/django-isomorphic.svg)
[![codecov.io](http://codecov.io/github/wildfish/django-isomorphic/coverage.svg?branch=master)](http://codecov.io/github/wildfish/django-isomorphic?branch=master)


*Note* The server has to be restarted for template updates as the templates are cached on the template server if you are using React.

It's important to know that the context is available on the client side, so putting sensitive data in the context is a bad idea.

The template server is using a Unix domain socket. 
This means that the server will not run on windows, and the server is not accessible outside of the machine it's running on.


## Why?

There are few easy to use libraries for rendering JavaScript server side for Django.
The aim is to create a solution that requires as little setup as possible and performs well.


## Docs

See [Docs](/docs/README.md)

