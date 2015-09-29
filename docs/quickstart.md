# Quick start

For installation instructions see the [installation instructions](/docs/installation.md).

## Configuration

Add the template backend to settings.

```python
TEMPLATES = [
    ...
    {
        'BACKEND': 'isomorphic.template.backend.JsTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'static/js/')
        ]
    }
]
```

and add `isomorphic` to `INSTALLED_APPS`.


## Creating a JavaScript template

When using the default React template renderer make sure the component is the only object exported.

```javascript
var React = require('react');

var Template = React.createClass({
    render: function() {
        return <div>A template</div>
    }
});

module.exports = Template;
```


## Using the React component in a template

Load the template tag: `{% load static djangojs %}`.

By calling `{% include_js 'template.js' %}` the template is rendered on the server and output to the template, much like the default `{% include 'template.html' %}`.


```html
{% load djangojs %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<h1>This is a Django template</h1>

{% include_js 'template.js' %}

</body>
</html>
```

