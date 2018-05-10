from .. import app, db,login_manager
from flask import request, current_app, jsonify,make_response
from ..models import Account, Student, Instructor, Leader
from flask_login import login_user, logout_user, current_user,login_required
from . import main

login_manager.login_view = 'main.no_login'


@main.route('/no_login')
def no_login():
    return "no login", 404


@main.route('/login', methods=['POST'])
def login():
    data = request.form
    account = data['account']
    user = Account.query.filter(account=account).first()
    if user is not None:
        if user.password == data['password']:
            s = Student.query.filter_by(id=account).first()
            if s is not None:
                login_user(s, remember=data['remember_me'])
                return jsonify({'type': 'student'})
            i = Instructor.query.filter_by(id=account).first()
            if i is not None:
                login_user(i, remember=data['remember_me'])
                return jsonify({'type': 'instructor'})
            l = Leader.query.filter_by(id=account).first()
            if l is not None:
                login_user(l, remember=data['remember_me'])
                return jsonify({'type': 'leader'})
            if account in app.config['FLASKY_ADMIN']:
                login_user(user, remember=data['remember_me'])
                return jsonify({'type:admin'})
            return jsonify({'message': 'type error'}), 400
        return jsonify({'message': 'password error'}), 403
    return jsonify({'message': 'no account'}), 404


@main.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user(current_user)
    return jsonify({'message': 'logout successful'})


@main.route('/change_passwd')
@login_required
def change_passwd():
    data = request.form
    u_account = Account.query.filter_by(current_user.account).first()
    old_password = u_account.password
    if old_password is None:
        return jsonify({'message': 'no account'}), 404
    if old_password == data.get('old_password'):
        u_account.password = data['new_password']
        db.session.add(u_account)
        db.session.commit()
        return jsonify({'message': 'change successful'})
    else:
        return jsonify({'message': 'password error'}), 403
