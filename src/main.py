import os
import random
import logging
import sqlite3

from flask import Flask, jsonify, request, render_template, make_response, abort, redirect, url_for, Blueprint
from werkzeug.routing import Rule

app = Flask(__name__, template_folder='templates')
DATABASE = 'users.db'
logging.basicConfig(filename='app.log', level=logging.INFO)


# API with a basic route and function
@app.route('/')
def hello_world():
    return 'Hello, World!'


# API with route variables
@app.route('/users/<username>')
def show_user_profile(username):
    return f'User {username}'


# API with query parameters
@app.route('/query')
def query_example():
    name = request.args.get('name')
    age = request.args.get('age')
    return jsonify({'name': name, 'age': age})


# API with a POST request and form data
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    return f'Username: {username}, Password: {password}'


# API with a GET request and headers
@app.route('/headers')
def headers():
    user_agent = request.headers.get('User-Agent')
    return f'User-Agent: {user_agent}'


# API with custom error handling
@app.route('/error')
def error():
    abort(404)


@app.errorhandler(404)
def not_found_error(err):
    return jsonify({'error': 'Not found ' + err}), 404


# API with file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    uploaded_file.save(uploaded_file.filename)
    return f'File {uploaded_file.filename} uploaded successfully'


# API with JSON data
@app.route('/json', methods=['POST'])
def json_example():
    data = request.get_json()
    return jsonify({'data': data})


# API with cookies
@app.route('/cookies')
def cookies():
    username = request.cookies.get('username')
    return f'Username: {username}'


@app.route('/setcookie')
def setcookie():
    resp = jsonify({'message': 'Cookie set'})
    resp.set_cookie('username', 'flaskuser')
    return resp


# API with render_template
@app.route('/template')
def template():
    return render_template('index.html')


# API with make_response
@app.route('/response')
def response():
    rsp = make_response('This is a response')
    rsp.headers['Content-Type'] = 'text/plain'
    return rsp


# API with redirect
@app.route('/redirect')
def redirect_example():
    return redirect(url_for('hello_world'))


# API with URL building
@app.route('/url')
def url():
    this_url = url_for('hello_world', _external=True)
    return f'The URL is {this_url}'


# API with dynamic URL building
@app.route('/user/<int:user_id>')
def user_profile(user_id):
    return f'Profile page of user {user_id}'


# API with route mapping
@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'


@app.route('/<name>')
def index(name):
    if name == 'projects':
        return redirect(url_for('projects'))
    elif name == 'about':
        return redirect(url_for('about'))
    else:
        abort(404)


# API with before_request
@app.before_request
def before_request():
    print('This is executed before each request.')


@app.route('/before')
def before():
    return 'This is a before_request example.'


# API with after_request
@app.after_request
def after_request(rsp):
    print('This is executed after each request.')
    return rsp


@app.route('/after')
def after():
    return 'This is an after_request example.'


# Using Werkzeug to define routes
def hello_world_werkzeug(req):
    return 'Hello, werkzeug! ' + req.headers


app.url_map.add(Rule('/', endpoint='hello_world_werkzeug', methods=['GET']))
app.view_functions['hello_world_werkzeug'] = hello_world_werkzeug


# Using Flask's stack method to define routes
@app.route('/users')
@app.route('/users/<username>')
def show_user_profile_stacked(username=None):
    if username:
        return f'User {username}'
    else:
        return 'All users'


# Using Flask's blueprint to group routes
users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/')
def users():
    return 'All users'


@users_bp.route('/<username>')
def user_profile(username):
    return f'Profile page of user {username}'


app.register_blueprint(users_bp)


# Command injection:
@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    rsp = os.system("ping -c 1 " + ip)
    return "Ping response: " + str(rsp)


# SQL Injection
@app.route('/user')
def user():
    username = request.args.get('username')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username='" + username + "'")
    user_data = cursor.fetchone()
    conn.close()
    return str(user_data)


# Log forging
@app.route('/login_vulnerable', methods=['POST'])
def login_vulnerable():
    username = request.form['username']
    password = request.form['password']
    if username and password:
        logging.info('Successful login attempt for user: ' + username)
        return "Login successful!"
    else:
        logging.info('Failed login attempt for user: ' + username)
        return "Login failed."


# Insecure randomness
@app.route('/random_number', methods=['GET'])
def random_number():
    return str(random.randint(1, 10))


if __name__ == '__main__':
    app.run(debug=True)
