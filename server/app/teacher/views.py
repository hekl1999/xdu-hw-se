from flask import current_app, request, jsonify
from ..models import *
from flask_login import current_user, login_required
from .. import app, db
from . import teacher


@teacher.route('/tea_class_info')
@login_required
def tea_class():
    tea_infos = Teach.query.all()
    if len(tea_infos) == 0:
        return jsonify({'message':'no class'}), 404
    else:
        result= []
        for tea_info in tea_infos:
            re = {'class_id': tea_info.classes.id,
                  'course_id': tea_info.classes.course.id,
                  'course_name': tea_info.classes.course.name,
                  'type': tea_info.classes.course.type}
            schs = Schedule.query.filter_by(class_id=tea_info.classes.id).all()
            re_day = [s.day for s in schs]
            re['day'] = re_day
            result.append(result)
        return jsonify(result)


@teacher.route('/tea_class_info')
@login_required
def class_info():
    class_id = request.data.get('class_id')
    if class_id is None:
        return jsonify({'message':'no data'}),401
    teas = Teach.query.filter_by(class_id=class_id).all()
    if current_user.id  not in [teach.teacher.id for teach in teas]:
        return jsonify({'message':'you are not this class teacher'}), 403
    student_infos = Schedule.query.filter_by(class_id= class_id).all()
    result = []
    for student_info in student_infos:
        re = {'student_id':student_info.student.id,
              'student_name':student_info.student.name,
              'grade':student_info.grade}
        result.append(re)
    return jsonify(result)


@teacher.route('/')