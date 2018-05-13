from . import student
from .. import db, login_manager
from ..models import *
from flask import request, jsonify
from flask_login import current_user, login_required,login_manager
login_manager.login_view = 'main.no_login'


@student.route('/stu_mine_class',methods=['GET'])
@login_required
def mine_class():
    result = []
    my_classes = Curricula_variable.query.filter_by(student_id=current_user.id).all()
    if len(my_classes) > 0:
        for c in my_classes:
            cl = {}
            class_id = c.class_id
            sch = Schedule.query.filter_by(class_id=class_id).first()
            tea = Teach.query.filter_by(class_id=class_id).all()
            cou = Course.query.filter_by(class_id=class_id).first()
            if sch is None or len(tea) == 0 or cou is None:
                return jsonify({'message': 'data missing'}), 404
            cl['classroom_id'] = sch.classroom_id
            cl['week'] = sch.week
            cl['day'] = sch.day
            cl['section'] = sch.section
            instructors = []
            for t in tea:
                teacher = Instructor.query.filter_by(id=t.instructor_id).first().name
                instructors.append(teacher)
            cl['instructors_name'] = instructors
            cl['course_id'] = cou.id
            cl['course_name'] = cou.name
            result.append(cl)
        return jsonify(result)
    return jsonify({'message': 'no course'}), 404


@student.route('/stu_mine_grade',methods=['GET'])
@login_required
def mine_grade():
    result=[]
    my_classes = Curricula_variable.query.filter_by(student_id = current_user.id).all()
    if len(my_classes) > 0:
        for my_class in my_classes:
            cl = {}
            cl['grade'] = my_class.grade
            class_info = Class.query.filter_by(id=my_class.class_id).first()
            course_info = Course.query.filter_by(id=class_info.course_id).first()
            cl['course_id'] = course_info.id
            cl['name'] = course_info.name
            cl['type'] = course_info.type
            cl['credit'] = course_info.credit
            result.append(cl)
        return jsonify(result)
    return jsonify({'message': 'no course'}), 404
