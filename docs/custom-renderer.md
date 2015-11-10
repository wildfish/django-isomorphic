# Creating a custom renderer

It is possible (and simple) to create a custom template renderer, making it possible to render templates using other engines, such as Handlebars etc.

Specify the path to the renderer in settings:

```python
DJANGO_ISOMORPHIC_RENDERER  = os.path.join(BASE_DIR, 'custom_renderer/custom.js')
```

The custom renderer has to implement at least one function: `render` that takes three arguments:

*  templatePath
*  context
*  request

An example custom template renderer:

```javascript
var renderer = {
    render: function(templatePath, context, request) {
        return 'This is a custom template renderer';
    }
};

module.exports = renderer;
```
