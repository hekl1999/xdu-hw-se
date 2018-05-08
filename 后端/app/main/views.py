from flask import request, current_app, jsonify
from ..models import Account, Student, Instructor
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
            type = data['type']
            if type == 'student':
                s = Student.query.filter_by(id=account).first()
                if s is not None:
                    login_user(s, data['remember_me'])
                    return jsonify({'type': 'student'}), 200
                else:
                    return jsonify({'message': 'type error'}), 200
            elif type == 'instructor':
                i = Instructor.query.filter_by(id=account).first()
                if i is not None:
                    login_user(i, data['remember_me'])
                    return jsonify({'type': 'instructor'}), 200
                else:
                    return jsonify({'message': 'type error'}), 200
            elif type in ['admin', 'leader']:
                login_user(user, remember=data['remember_me'])
                return jsonify({'type': type}), 200
            else:
                return jsonify({'message': 'type error'}), 200
        else:
            return jsonify({'message': 'password wrong'})
    else:
        return jsonify({'message': 'no user'})
