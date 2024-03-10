"""entry point for web app"""
import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
    """index page"""
#    print('Request for index page received')
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    """favicon"""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['GET'])
def hello_get():
    """get demo for hello"""
    return "Hello Get"


@app.route('/hello', methods=['POST'])
def hello():
    """post demo for hello"""
    name = request.form.get('name')

    if name:
        return render_template('hello.html', name=name)

    print('Request for hello page received with no name or blank name -- redirecting')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
