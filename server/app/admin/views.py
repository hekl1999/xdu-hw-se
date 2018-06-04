from ..models import *
from .. import db,app
from flask_login import login_required
from . import admin
from flask import jsonify, request


@admin.route('/account_list')
@login_required
def account_list():
    all_accounts = Account.query.all()
    all_students = Student.query.filter(Student.id.in_([student.account for student in all_accounts
                                                        if student.type == 'student'])).all()
    result = [{'account': student.id, 'name': student.name, 'type': 'student'}
              for student in all_students]
    all_instructors = Instructor.query.filter(Instructor.id.in_([instructor.account for instructor in all_accounts
                                                                 if instructor.type == 'instructor']))
    result += [{'account': instructor.id, 'name': instructor.name, 'type': 'instructor'}
               for instructor in all_instructors]
    all_admins = Admin.query.filter(Admin.id.in_([admin.account for admin in all_accounts
                                                  if admin.type == 'admin']))
    all_superiors = Superior.query.filter(Superior.id.in_([superior.account for superior in all_accounts
                                                          if superior.type == 'superior']))
    result = result + [{'account': admin.id, 'name': admin.name, 'type': 'admin'}
                       for admin in all_admins] + \
             [{'account': superior.id, 'name': superior.name, 'type': 'superior'}
              for superior in all_superiors]
    return jsonify(result)


@admin.route('/exam_info', methods=['POST', 'GET'])
@login_required
def get_exam():
    exam_id = request.form.get('exam_id')
    if exam_id is None:
        exam_rooms = Exam_room.query.all()
        result = []
        for exam_room in exam_rooms:
            re = {
                'exam_id': exam_room.exam.id,
                'date': exam_room.exam.date,
                'time': exam_room.exam.time,
                'classroom_id': exam_room.classroom_id,
                'class_id': exam_room.exam.classes_id
            }
            result.append(re)
        return jsonify(result)
    else:
        exam_info = Exam.query.filter_by(id=exam_id).first()
        if exam_info is None:
            return jsonify({'message': 'no exam'}), 404
        result = {
            'exam_id': exam_id,
            'date': exam_info.date,
            'time': exam_info.time,
            'class_id': exam_info.classes.id,
            'classroom_id': Exam_room.query.filter_by(exam_id=exam_id).first().classroom.id,
            'course_id': exam_info.classes.course.id,
            'course_name': exam_info.classes.course.name,
            'instructor_name': [teacher.teacher.name for teacher in
                                Teach.query.filter_by(class_id=exam_info.classes.id).all()],
            'student': [{'student_id': student.student.id, 'name': student.student.name}
                        for student in CurriculaVariable.query.filter_by(class_id= exam_info.classes.id).all()]
        }
        return jsonify(result)


@admin.route('/class_list', methods=['POST', 'GET'])
@login_required
def get_class_list():
    class_id = request.form.get('class_id')
    if class_id is None:
        all_classes = Class.query.all()
        result = [
            {'class_id': class_info.id,
             'course_id': class_info.course.id,
             'course_name': class_info.course.name,
             'instructor_name': [teacher.teacher.name for teacher in
                                Teach.query.filter_by(class_id=class_info.id).all()],
             'classroom_id': Schedule.query.filter_by(class_id=class_info.id).first().classroom_id
             }
            for class_info in all_classes
        ]
        return jsonify(result)
    else:
        class_info = Class.query.filter_by(id=class_id).first()
        if class_info is None:
            return jsonify({'message': 'no class'}), 404
        result = {
            'class_id': class_id,
            'classroom_id': Schedule.query.filter_by(class_id=class_info.id).first().classroom_id,
            'instructor_name': [teacher.teacher.name for teacher in
                                Teach.query.filter_by(class_id=class_info.id).all()],
            'course_info': {
                'course_id': class_info.course.id,
                'course_name': class_info.course.name,
                'type': class_info.course.type,
                'credit': class_info.course.credit,
                'period': class_info.course.period,
            },
            'student': [{'student_id': student.student.id,
                        'student_name': student.student.name}
                        for student in CurriculaVariable.query.filter_by(class_id=class_info.id).all()]
        }
        return jsonify(result)
