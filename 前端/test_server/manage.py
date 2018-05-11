from flask import Flask, request, g, redirect, session
from flask.ext.cors import CORS
import os
import sqlite3
import json

DATABASE = 'db.sqlite'
SECRET_KEY = os.urandom(233)
app = Flask(__name__)
CORS(app)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/login')
def login():
    account = request.form.get('account')
    passwd = request.form.get('passwd')
    print(account, passwd)
    if account == passwd:
        if account in ('instructor', 'student', 'admin', 'root'):
            return account, 200
        else:
            return 'no_one', 404
    else:
        return 'passwd_wrong', 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
