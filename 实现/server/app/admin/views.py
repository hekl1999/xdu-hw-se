from ..models import *
from .. import db, app
from flask_login import login_required
from . import admin
from flask import jsonify, request
import json


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


@admin.route('/exam_info/')
@login_required
def get_exam():
    exam_id = request.args.get('exam_id')
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
        print(result)
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


@admin.route('/class_list/')
@login_required
def get_class_list():
    class_id = request.args.get('class_id')
    print(class_id)
    if class_id is None:
        all_classes = Class.query.all()
        result = [
            {'class_id': class_info.id,
             'course_id': class_info.course.id,
             'course_name': class_info.course.name,
             'instructor_name': [teacher.teacher.name for teacher in
                                 Teach.query.filter_by(class_id=class_info.id).all()],
             }
            for class_info in all_classes
        ]
        print(result)
        return jsonify(result)
    else:
        class_info = Class.query.filter_by(id=class_id).first()
        if class_info is None:
            return jsonify({'message': 'no class'}), 404
        result = {
            'class_id': class_id,
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
        if Schedule.query.filter_by(class_id=class_id).first() is not None:
            result['classroom_id'] = Schedule.query.filter_by(class_id=class_id).first().classroom_id
        else:
            result['classroom_id'] = None
        return jsonify(result)


@admin.route('/course_list')
@login_required
def get_course_list():
    return jsonify([{'course_id': course.id,
                     'course_name': course.name,
                     'type': course.type,
                     'credit': course.credit,
                     'period': course.period}
                    for course in Course.query.all()
                    ])


@admin.route('/schedule_list')
@login_required
def get_schedule_list():
    all_schedule = Schedule.query.all()
    result = []
    for schedule in all_schedule:
        re = {
              'schedule_id': schedule.id,
              'class_id': schedule.class_id,
              'course_name': schedule.classes.course.name,
              'classroom_id': schedule.classroom_id,
              'week': schedule.week,
              'day': schedule.day,
              'section': schedule.section}
        result.append(re)
    return jsonify(result)


@admin.route('/change_account', methods=['POST', 'GET'])
@login_required
def change_account():
    post_data = json.loads(request.data.decode())
    change_type = post_data.get('change_type')
    if change_type == 'DELETE':
        detail = post_data.get('detail')
        delete_account = Account.query.get(int(detail.get('account')))
        post_type = detail.get('type')
        try:
            if delete_account is not None:
                db.session.delete(delete_account)
                db.session.commit()
                if post_type == 'student':
                    delete_student = Student.query.get(int(detail.get('account')))
                    db.session.delete(delete_student)
                    db.session.commit()
                elif post_type == 'instructor':
                    delete_teacher = Instructor.query.get(int(detail.get('account')))
                    db.session.delete(delete_teacher)
                    db.session.commit()
                elif post_type == 'superior':
                    delete_superior = Superior.query.get(int(detail.get('account')))
                    db.session.delete(delete_superior)
                    db.session.commit()
                elif post_type == 'admin':
                    delete_admin = Admin.query.get(int(detail.get('account')))
                    db.session.delete(delete_admin)
                    db.session.commit()
                return jsonify({'message': 'delete ok'})
            else:
                return jsonify({'message': 'no account'}), 404
        except:
            return jsonify({'message': '罗大佬劝你再看看'}), 403
    if change_type == 'UPDATE':
        detail = post_data.get('detail')
        post_account = detail.get('account')
        if post_account is None:
            return jsonify({'message': 'no account'}), 401
        update_account = Account.query.filter_by(account=post_account).first()
        if update_account is None:
            return jsonify({'message': 'no account'}), 404
        post_type = detail.get('type', update_account.type)
        post_passwd = detail.get('passwd', update_account.password)
        update_account.password = post_passwd
        update_user = None
        if post_type == 'student':
            update_user = Student.query.filter_by(id=post_account).first()
        elif post_type == 'instructor':
            update_user = Instructor.query.filter_by(id=post_account).first()
        elif post_type == 'admin':
            update_user = Admin.query.filter_by(id=post_account).first()
        elif post_type == 'superior':
            update_user = Superior.query.filter_by(id=post_account).first()
        if update_user is not None:
            update_user.name = detail.get('name', update_user.name)
        else:
            return jsonify({'message': 'no user'}), 404
        db.session.add(update_account)
        db.session.add(update_user)
        db.session.commit()
        return jsonify({'message': 'update ok'})
    if change_type == 'INSERT':
        detail = post_data.get('detail')
        post_account = detail.get('account')
        post_name = detail.get('name')
        post_type = detail.get('type')
        post_passwd = detail.get('passwd')
        if post_account is None or post_type is None or post_name is None or post_passwd is None:
            return jsonify({'message': 'data missing'}), 403
        insert_account = Account(account=post_account,type=post_type,password=post_passwd)
        if post_type == 'student':
            insert_user = Student(id=post_account, name=post_name, year=detail.get('year', 2018))
            print(insert_user)
            db.session.add(insert_user)
            db.session.commit()
        elif post_type == 'instructor':
            insert_user = Instructor(id=post_account, name=post_name)
            db.session.add(insert_user)
            db.session.commit()
        elif post_type == 'admin':
            insert_user = Admin(id=post_account, name=post_name)
            db.session.add(insert_user)
            db.session.commit()
        elif post_type == 'superior':
            insert_user = Superior(id=post_account, name=post_name)
            db.session.add(insert_user)
        db.session.add(insert_account)
        db.session.commit()
        return jsonify({'message': 'insert OK'})


@admin.route('/change_course', methods=['POST', 'GET'])
@login_required
def change_course():
    post_data = json.loads(request.data.decode())
    change_type = post_data.get('change_type')
    # 我真想知道会有谁发个空的type给我
    if change_type == 'DELETE':
        try:
            delete_id = post_data.get('detail').get('course_id')
            delete_course = Course.query.filter_by(id=delete_id).first()
            db.session.delete(delete_course)
            db.session.commit()
            return jsonify({'message': 'delete ok'})
        except:
            return jsonify({'message': '罗大佬劝你想清楚在删'}), 403
    if change_type == 'UPDATE':
        detail = post_data.get('detail')
        update_course = Course.query.filter_by(id=detail.get('course_id')).first()
        update_course.name = detail.get('course_name', update_course.name)
        update_course.credit = detail.get('credit', update_course.credit)
        update_course.type = detail.get('type', update_course.type)
        update_course.period = detail.get('period', update_course.period)
        db.session.add(update_course)
        try:
            db.session.commit()
            return jsonify({'message': 'update ok'})
        except:
            db.session.rollback()
            return jsonify({'message': 'update wrong'}), 403
    if change_type == 'INSERT':
        detail = post_data.get('detail')
        insert_course = Course(id=detail.get('course_id'),
                               name=detail.get('course_name'),
                               type=detail.get('type'),
                               credit=detail.get('credit'),
                               period=detail.get('period'))
        db.session.add(insert_course)
        try:
            db.session.commit()
            return jsonify({'message': 'insert ok'})
        except:
            db.session.rollback()
            return jsonify({'message': 'insert wrong'}), 403
    return jsonify({'message': 'losing type'}), 403


@admin.route('/change_schedule', methods=['POST', 'GET'])
@login_required
def change_schedule():
    post_data = json.loads(request.data.decode())
    change_type = post_data.get('change_type')
    detail = post_data.get('detail')
    if change_type == 'DELETE':
        delete_id = detail.get('schedule_id')
        delete_schedule = Schedule.query.get(delete_id)
        try:
            db.session.delete(delete_schedule)
            db.session.commit()
            return jsonify({'message': 'delete ok'})
        except:
            db.session.rollback()
            return jsonify({'message': '罗大佬说不行'}), 403
    if change_type == 'UPDATE':
        update_schedule = Schedule.query.filter_by(id=detail.get('schedule_id')).first()
        print(update_schedule.classes.id)
        print(update_schedule.classroom.id)
        update_classes = Class.query.filter_by(
            id=detail.get('class_id', update_schedule.classes.id)).first()
        update_classroom = Classroom.query.filter_by(
            id=detail.get('classroom_id', update_schedule.classroom.id)).first()
        update_schedule.week = detail.get('week', update_schedule.week)
        update_schedule.day = detail.get('day', update_schedule.day)
        update_schedule.section = detail.get('section', update_schedule.section)
        if update_classroom is not None:
            update_schedule.classroom = update_classroom
        if update_classes is not None:
            update_schedule.classes = update_classes
        if update_classes is None or update_classroom is None:
            return jsonify({'message': 'data error'}), 403
        try:
            db.session.add(update_schedule)
            db.session.commit()
            return jsonify({'message': 'update ok'})
        except:
            db.session.rollback()
            return jsonify({'message': '罗大佬说不ok'}), 403
    if change_type == 'INSERT':
        insert_class = Class.query.filter_by(id=detail.get('class_id')).first()
        insert_classroom = Classroom.query.filter_by(id=detail.get('classroom_id')).first()
        insert_week = detail.get('week')
        insert_day = detail.get('day')
        insert_section = detail.get('section')
        if insert_class is None or insert_classroom is None \
                or insert_week is None or insert_day is None \
                or insert_section is None:
            return jsonify({'message': 'some data missing'}), 403
        insert_schedule = Schedule(classes=insert_class, classroom=insert_classroom, week=insert_week,
                                   day=insert_day, section=insert_section)
        try:
            db.session.add(insert_schedule)
            db.session.commit()
            return jsonify({'message': 'insert ok'})
        except:
            db.session.rollback()
            return jsonify({'message': '罗大佬说不OK'}), 403
