from flask import Flask, request, g, redirect, session
from flask_cors import CORS
import os
import sqlite3
import json

DATABASE = 'db.sqlite'
SECRET_KEY = os.urandom(233)
app = Flask(__name__)
CORS(app, supports_credentials=True, origin=['127.0.0.1', 'localhost'])
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


@app.route('/login', methods=['POST'])
def login():
    account = request.form.get('account')
    passwd = request.form.get('password')
    if account == passwd:
        if account in ('instructor', 'student', 'admin', 'root'):
            data = {'type': account}
            return json.dumps(data), 200
        else:
            return 'no_one', 404
    else:
        return 'passwd_wrong', 403


@app.route('/who_am_i')
def who_am_i():
    data = {'type': 'student', 'name': 'hhh'};
    return json.dumps(data), 200


@app.route('/change_passwd', methods=['POST'])
def change_passwd():
    o_passwd = request.form.get('old_password')
    n_passwd = request.form.get('new_password')
    if not o_passwd or not n_passwd:
        return 'bad', 400
    else:
        return '', 401


@app.route('/logout')
def logout():
    return '', 200


@app.route('/student/mine_grade')
def stu_mine_grade():
    data = [{
        'course_id': 'SE3002L-02',
        'name': '信号与系统',
        'type': 4,
        'credit': 2,
        'grade': 70
    }, {
        'course_id': 'SE5003L-02',
        'name': '数据库系统',
        'type': 1,
        'credit': 2,
        'grade': -1
    }, {
        'course_id': 'SE2007L-02',
        'name': '面向对象程序设计',
        'type': 1,
        'credit': 2,
        'grade': 89
    }, {
        'course_id': 'SE3003L-02',
        'name': '数字电路与系统设计',
        'type': 1,
        'credit': 1,
        'grade': 100
    }, ]
    return json.dumps(data), 200


@app.route('/student/mine_class')
def stu_mine_class():
    data = [{
        'course_id': 'SE3002L-02',
        'course_name': '信号与系统',
        'instructor_name': ['张玲霞（副教授）', ],
        'classroom_id': 'A-325',
        'week': 1,
        'day': 1,
        'section': 1
    }, {
        'course_id': 'SE5003L-02',
        'course_name': '数据库系统',
        'instructor_name': ['刘伟（副教授）', ],
        'classroom_id': 'B-106',
        'week': 1,
        'day': 1,
        'section': 2
    }, {
        'course_id': 'SE2007L-02',
        'course_name': '面向对象程序设计',
        'instructor_name': ['王献青（副教授）', '韦统义（副教授）', ],
        'classroom_id': 'A-314',
        'week': 1,
        'day': 1,
        'section': 3
    }, {
        'course_id': 'SE3003L-02',
        'course_name': '数字电路与系统设计',
        'instructor_name': ['张亮（副教授）', ],
        'classroom_id': 'B-419',
        'week': 1,
        'day': 2,
        'section': 1
    }, ]
    return json.dumps(data), 200


@app.route('/student/exam_info')
def stu_exam_info():
    data = [{
        'course_name': '数字电路与系统设计',
        'classroom_id': 'A-311',
        'date': '2018-03-23',
        'time': '20:00:00',
        'exam_grade': 20
    }, {
        'course_name': '数字电路与系统设计',
        'classroom_id': 'A-311',
        'date': '2018-03-23',
        'time': '20:00:00',
        'exam_grade': 80
    }, {
        'course_name': '数字电路与系统设计',
        'classroom_id': 'A-311',
        'date': '2018-03-23',
        'time': '20:00:00',
        'exam_grade': 90
    }, {
        'course_name': '数字电路与系统设计',
        'classroom_id': 'A-311',
        'date': '2018-03-23',
        'time': '20:00:00',
        'exam_grade': -1
    }, ]
    return json.dumps(data), 200


@app.route('/teacher/mine_class')
def tea_mine_class():
    data = [{
        'class_id': 'SE3002L-02',
        'course_id': 'SE3002L',
        'course_name': '信号与系统',
        'classroom_id': 'A-325',
        'week': 1,
        'day': 1,
        'section': 1
    }, {
        'class_id': 'SE5003L-02',
        'course_id': 'SE5003L',
        'course_name': '数据库系统',
        'classroom_id': 'B-106',
        'week': 1,
        'day': 1,
        'section': 2
    }, {
        'class_id': 'SE2007L-02',
        'course_id': 'SE2007L',
        'course_name': '面向对象程序设计',
        'classroom_id': 'A-314',
        'week': 1,
        'day': 1,
        'section': 3
    }, {
        'class_id': 'SE3003L-02',
        'course_id': 'SE3003L',
        'course_name': '数字电路与系统设计',
        'classroom_id': 'B-419',
        'week': 1,
        'day': 2,
        'section': 1
    }, ]
    return json.dumps(data), 200


@app.route('/teacher/class_info')
def tea_class_info():
    if request.args.get('class_id'):
        data = [
            {'student_id': '16130120191', 'student_name': '罗阳豪', 'grade': 100},
            {'student_id': '16130120201', 'student_name': '方浩杰', 'grade': 80},
            {'student_id': '16130120181', 'student_name': '郑昊鹏', 'grade': -1},
            {'student_id': '16130120181', 'student_name': '郑昊鹏', 'grade': -1},
            {'student_id': '16130120181', 'student_name': '郑昊鹏', 'grade': -1},
        ]
    else:
        data = [{
            'class_id': 'SE3002L-01',
            'course_id': 'SE3002L',
            'course_name': '信号与系统',
            'type': 4,
            'classroom_id': 'A-325',
            'time': [{'day': 1, 'section': 2}, {'day': 3, 'section': 4}],
        }, {
            'class_id': 'SE3002L-02',
            'course_id': 'SE3002L',
            'course_name': '信号与系',
            'type': 4,
            'classroom_id': 'A-325',
            'time': [{'day': 2, 'section': 2}, {'day': 3, 'section': 4}],
        }, {
            'class_id': 'SE3002L-03',
            'course_id': 'SE3002L',
            'course_name': '信号与系统',
            'type': 4,
            'classroom_id': 'A-325',
            'time': [{'day': 3, 'section': 2}, {'day': 3, 'section': 4}],
        }, {
            'class_id': 'SE3002L-04',
            'course_id': 'SE3002L',
            'course_name': '信号与系统',
            'type': 4,
            'classroom_id': 'A-325',
            'time': [{'day': 4, 'section': 2}, {'day': 3, 'section': 4}],
        },
        ]
    return json.dumps(data), 200


@app.route('/teacher/insert_grade', methods=['POST'])
def tea_insert_grade():
    print(request.get_data())
    return '', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
