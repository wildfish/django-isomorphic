## Table of contents

*  [Installation](/docs/installation.md)
*  [Quick start](/docs/quickstart.md)
*  [Custom renderer](/docs/custom-renderer.md)
*  [Settings](/docs/settings.md)


## Usage

*Note* ES6 templates needs to be "transpiled".

The template server starts automatically, this can be disabled by setting `DJANGO_ISOMORPHIC_AUTOSTART` to False.
To manually start the server run `node /path/to/django-isomorphic/javascript/dist/template-server.js`.

It's possible to use the template as part of a Django template, or it can entirely replace Django template. 


### Using as part of a Django template

In a template:

```html
{% load djangojs %}
...
{% include_js 'foo.js' bar='hello' baz='world' %}
```

### Pure React components as templates

When using the react renderer, make sure the component is the default export

e.g 

```javascript
// ES6
export default class Foo extends React.Component { ... }

// CommonJS
module.exports = React.Component { ... }
```


## The template tag

The template tag `include_js` takes at least one parameter: the template name.

Alternative named parameters can be passed and will be available in the template.

E.g: `{% include_js 'foo.js' bar='hello' baz='world' %}`

```javascript
var bar = this.props.bar; // <-- 'hello'
```


## Additional info

If you see the warning:

> Warning: render(): Target node has markup rendered by React, but there are unrelated nodes as well. This is most commonly caused by white-space inserted around server-rendered markup

when using React, remove any white space around the element surrounding the `include_js` output.

e.g

change

```html
<div id="stuff">
    {% include_js 'something.js' data=data %}
</div>
```

to

```html
<div id="stuff">{% include_js 'something.js' data=data %}</div>
```
