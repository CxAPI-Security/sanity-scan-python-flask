import subprocess

from flask import Flask, Blueprint, request, jsonify
from markupsafe import escape
from werkzeug.routing import Rule

app = Flask(__name__)


# Default route
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# Path parameter - default
@app.route("/param/<name>")
def hello(name):
    subprocess.call("grep -R {} .".format(name), shell=True)  # command injection
    return f"Hello, {escape(name)}!"


# Path parameter - specific type
@app.route('/blog/<int:post_id>')
def show_blog(post_id):
    return 'Blog Number %d' % post_id


# POST HTTP method
@app.route('/user', methods=["POST"])
def user():
    password = request.json['password']  # sensitive data
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com',
                    'password': password})


# Stacking routes
@app.route('/hello/')
@app.route('/hello/<name>')
def stacked(name=None):
    name = name if name else "No name"
    return f"Hello, {escape(name)}!"


# Endpoint rule - Werkzeug
app.url_map.add(Rule('/custom', endpoint='custom'))


@app.endpoint('custom')
def my_index():
    return "Hello custom"


# app ad durl rule
def extra():
    return 'Extra rule'


app.add_url_rule('/extra', 'extra', extra)


# Custom decorator
def my_decorator(func):
    app.add_url_rule('/mydec', func.__name__, func)
    return func()


@my_decorator
def my_decorator_example():
    return "<b>This should be bold</b>"


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
