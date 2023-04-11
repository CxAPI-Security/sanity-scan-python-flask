from flask import Flask, Request, Blueprint
from markupsafe import escape

app = Flask(__name__)


# Default route
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# Path parameter - default
@app.route("/param/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


# Path parameter - specific type
@app.route('/blog/<int:post_id>')
def show_blog(post_id):
    return 'Blog Number %d' % post_id


# Path parameter - specific type
@app.route('/rev/<float:rev_number>')
def revision(rev_number):
    return 'Revision Number %f' % rev_number


# Stacking routes
@app.route('/hello/')
@app.route('/hello/<name>')
def stacked(name=None):
    name = name if name else "No name"
    return f"Hello, {escape(name)}!"


# Endpoint rule - Werkzeug
from werkzeug.routing import Rule

app.url_map.add(Rule('/custom', endpoint='custom'))


@app.endpoint('custom')
def my_index():
    return "Hello custom"


# app ad durl rule
def extra():
    return 'Extra rule'


app.add_url_rule('/extra', 'extra', extra)


# Custom decorator
def mydecorator(func):
    app.add_url_rule('/mydec', func.__name__, func)
    return func()


@mydecorator
def mydecoratorexample():
    return "<b>This should be bold</b>"


# TODO
# Custom middleware
class Middleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        print('Custom middleware - path: %s, url: %s' % (request.path, request.url))
        return self.app(environ, start_response)


app.wsgi_app = Middleware(app.wsgi_app)

# Blueprint, before_request_funcs
api = Blueprint('my_blueprint', __name__)


def before_my_blueprint():
    print('runs before blueprint')  # kind of like before_request


@api.route('/blueprint')
def test():
    return 'Blueprint API'


app.before_request_funcs = {
    'my_blueprint': [before_my_blueprint]
}

app.register_blueprint(api)
