from flask import Flask
from datetime import datetime

#https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application

app = Flask(__name__)

@app.route("/")
def hello_world():
    return f"<p> Hello world at {datetime.now()} </p>"