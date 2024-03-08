"""main entry point for server api"""
from datetime import datetime
from flask import Flask

# https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application

app = Flask(__name__)


@app.route("/")
def hello_world():
    """return hello world: just for test"""
    return f"<p> Hello world at {datetime.now()} </p>"
