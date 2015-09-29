# Building an isomorphic single page app with Django and React

Building a website usually means either sacrificing SEO for better user experience, or downgrading the user experience for better SEO.
Isomorphic websites isn't a new concept, but building them in Django isn't always straight forward.

This post will go through the steps for building a single page app in Django using `django-isomorphic`: 
a server side JavaScript template renderer.


## System requirements
 
*  Python
*  Node


## Setup

Install Django 1.8 and django-isomorphic:

    pip install django django-isomorphic
    
Create a Django project: `django-admin startproject isodemo`.

Create a static directory where all the JavaScript files will go.

    cd isodemo
    mkdir static
    mkdir static/js
    
and a template directory for your base template (we'll use this to load the client side JavaScript).

    mkdir templates

Open settings.py and add the `django-isomorphic` template backend
    
    TEMPLATES = [
        ...
        {
            'BACKEND': 'isomorphic.template.backend.JsTemplates',
            'DIRS': [
                join(BASE_DIR, 'static/js/dist')
            ]
        }
    ]
    
and the `STATIC_URL` and `STATICFILES_DIRS` setting:
    
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    
and finally add `isomorphic` to `INSTALLED_APPS`
    
This is all the setup we have to do to render the JavaScript templates.


## Adding the views and some data

Create a views.py with the following code:

    from django.views.generic import TemplateView
    
    
    class Home(TemplateView):
        template_name = 'base.html'
    
    
    class DataList(TemplateView):
        template_name = 'base.html'
    
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['list_of_data'] = ['foo', 'bar', 'baz']
            return context


*note*: it would be more likely that the `DataList` view would return a list of serialized models, however for the sake
of brevity that part is replaced with a list of strings.

We use the same template on both views: `base.html`, as we'll let the template server decide which component to use 
based on a JavaScript router (which we'll create in a bit).

add the views to urls.py:

    urlpatterns = [
        url(r'^$', Home.as_view(), name='home'),
        url(r'^data/$', DataList.as_view(), name='data'),
        url(r'^admin/', include(admin.site.urls)),
    ]


## The template

Create a new template in `templates/` and name it base.html, and add the following code:
    
    {% load static djangojs %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title></title>
    </head>
    <body>
    <h1>This is a Django template</h1>
    
    {% include_js 'base.js' %}
    
    <script type="text/javascript" src="{% static 'js/dist/dist.js' %}"></script>
    </body>
    </html>


`{% include_js 'base.js' %}` will render the component on the server rather than on the client.


## Adding the JavaScript

In `static/js/` run the following:

*  `npm init --yes`.
*  `npm install react --save`
*  `npm install browserify --save-dev`
*  `npm install reactify --save-dev`
*  `npm install react-tools --save-dev`

The first command will tell `node` that this is a package.

The second command installs React and saves it as a dependency in package.json (you can think of dependencies in package.json as Python requirements in requirements.txt).

The third command installs Browserify, we need this because we have to write the components using CommonJS so `node` can understand them, and subsequently the template server.

The fourth command installs Reactify, which is a Browserify transformer, converting JSX into JavaScript.

The fifth (and final) command installs React tools, which can convert JSX into JavaScript, and this is needed for the server side rendering of JSX.

*note*: if JSX is not used then Reactify and React Tools can be omitted 

We use `--save` for React as we want that to be included in our final JavaScript files, and we use `--save-dev` for Browserify as we don't need it to be included, but we need it to build the JavaScript.


Add the following JavaScript files to `static/js/`

*  router.js
*  base.js 
*  app.js 
*  home.js
*  data.js
*  index.js


### Router.js

The router will take care of getting the right component for the url (kind of like urls.py).
Since we are making a single page application we need the urls to be available for both the server and the client.


    var Home = require('./home');
    var Data = require('./data');
    
    var router = {
        getComponent: function(pathname) {
            switch (pathname) {
                case '/':
                    return Home;
                case '/data/':
                    return Data;
                default :
                    return Home
            }
        }
    };
    
    module.exports = router;


### Base.js

The `Base` component is in charge of wrapping everything, so all components on the client renders the same as on the server.
By converting the `props` to JSON we can ensure that the same data from the server is available to the components on the client 
(we do this with the function `stringify`).

By using `dangerouslySetInnerHTML` React will output the return value from the function exactly as is, and won't escape anything.


    var React = require('react');
    var App = require('./app');
    
    var Base = React.createClass({
        stringify: function() {
            return {__html: "window.props=" + JSON.stringify(this.props)};
        },
    
        render: function() {
            return (
                <div>
                    <h1>Base component</h1>
                    <div id="app"><App {...this.props} /></div>
                    <script type="text/javascript" dangerouslySetInnerHTML={this.stringify()} />
                </div>
            )
        }
    });
    
    
    module.exports = Base;


### App.js

This is perhaps the most complicated component.
It does the following things:

*  Get the component based on the route (the requested path according to the server, or the url in the browsers address field)
*  Provide a click handler for any `<a>` tag that should trigger a change in navigation (e.g change url / change component)
    
    
    var React = require('react');
    var router = require('./router');
    
    var App = React.createClass({
        getInitialState: function () {
            return {pathname: this.props._request.path || '/'};
        },
    
        componentDidMount: function () {
            var _this = this;
            window.onpopstate = function (e) {
                _this.updateUrl(window.location.pathname);
            };
        },
    
        handleClick: function (e) {
            if (window.history.pushState !== undefined) {
                e.preventDefault();
                window.history.pushState(null, null, e.target.pathname + e.target.search);
                this.updateUrl(e.target.pathname);
            }
        },
    
        updateUrl: function (pathname) {
            this.setState({pathname: pathname});
        },
    
        getPathName: function () {
            return this.state.pathname;
        },
    
        render: function () {
            return (
                React.createElement(router.getComponent(this.getPathName()), {data: this.props, handleClick: this.handleClick})
            )
        }
    });
    
    module.exports = App;


The `App` component, which is rendered by the `base` component, acts like a wrapper around each child component, providing the 
child component with data and a click handler that can be used for navigation.


### Home.js

This is the most basic of the components, it simply outputs some html and provides a link to the data view.

    var React = require('react');
    
    var Home = React.createClass({
        getInitialState: function() {
            return this.props;
        },
    
        render: function() {
            return (
                <div>
                    <h2>Home</h2>
                    <p>This is the home view</p>
                    <a href="/data/" onClick={this.state.handleClick}>Data view</a>
                </div>
            )
        }
    });
    
    module.exports = Home;


### Data.js

This component is much the same as the `Home` component with the added bonus of outputting some data we received from our Django view.
In a real-world application `componentDidMount` would be a good place to fetch some data from an API. `componentDidMount` is not 
called on the server and would not trigger the API call, and the data is already provided by the view. 

    var React = require('react');
    
    var Data = React.createClass({
        getInitialState: function() {
            return this.props;
        },
    
        componentDidMount: function() {
            // Here data could be fetched from the server
            if (!this.state.data.list_of_data) {
                this.setState({
                    data: {
                        list_of_data: ['foo', 'bar', 'baz']
                    }
                });
            }
        },
    
        render: function() {
            var dataList = this.state.data.list_of_data || [];
    
            return (
                <div>
                    <h2>List of data</h2>
                    <a href="/" onClick={this.state.handleClick}>Home</a>
                    <ul>
                        {dataList.map(function(data, i) {
                            return <li key={"d-" + i}>{data}</li>
                        })}
                    </ul>
                </div>
            )
        }
    });
    
    module.exports = Data;


### index.js

The index.js is solely for the client, and it renders the `App` component and attaches it to the `<div>` in the `base` component that is rendered in base.html.

    var React = require('react');
    var App = require('./app');
    
    var Component = React.createFactory(App);
    
    React.render(
        Component(window.props),
        document.getElementById('app')
    );


## Putting it all together 

Since the server needs CommonJS modules, and the client (browser) doesn't work with CommonJS we need to use Browserify to convert the 
components to plain old JS for the browser.

This is done by running: `./node_modules/browserify/bin/cmd.js -t reactify -r react ./src/index.js -o ./dist/dist.js`

and the server can not handle JSX so we need to convert the JSX into plain JavaScript.
This is done by running: `./node_modules/react-tools/bin/jsx ./src ./dist`


## The final result

Start your local dev server: `./manage.py runserver` and browse to [http://localhost:8000](http://localhost:8000).
As you navigate between Home and Data you will notice that no GET requests are made to the server.

If you disable JavaScript in your browser it still works.
So any search engine indexing your website would hit /data/ (http://localhost:8000/data/) and all the content would still be available.

As an added bonus the site feels very quick to navigate since the views are already rendered.
