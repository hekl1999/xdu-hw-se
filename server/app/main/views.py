from .. import app, db
from flask import request, current_app, jsonify
from ..models import Account, Student, Instructor, Leader
from flask_login import login_user, logout_user, current_user
from . import main
import json


@main.route('/login', methods=['POST'])
def login():
    data = json.loads(request.post_data)
    account = data['account']
    user = Account.query.filter(account=account).first()
    if user is not None:
        if user.password == data['password']:
            s = Student.query.filter_by(id=account).first()
            if s is not None:
                login_user(s, remember=data['remember_me'])
                return jsonify({'type': 'student'}), 200
            i = Instructor.query.filter_by(id=account).first()
            if i is not None:
                login_user(i, remember=data['remember_me'])
                return jsonify({'type': 'instructor'}), 200
            l = Leader.query.filter_by(id=account).first()
            if l is not None:
                login_user(l, remember=data['remember_me'])
                return jsonify({'type': 'leader'}), 200
            if account in app.config['FLASKY_ADMIN']:
                login_user(user, remember=data['remember_me'])
                return jsonify({'type:admin'}), 200
            return jsonify({'message': 'type error'}), 200
        return jsonify({'message': 'password error'})
    return jsonify({'message': 'no account'})
