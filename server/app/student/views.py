from . import student
from .. import db, login_manager
from ..models import *
from flask import request, jsonify
from flask_login import current_user, login_required,login_manager
from datetime import datetime
login_manager.login_view = 'main.no_login'


@student.route('/stu_mine_class', methods=['GET'])
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


@student.route('/stu_mine_grade', methods=['GET'])
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


@student.route('/stu_class_list',methods=['GET'])
@login_required
def class_list():
    elective_courses = Course.query.filter_by(type != '1').all()
    result = []
    if len(elective_courses) == 0:
        return jsonify({'message':'no course'}), 404
    for e_c in elective_courses:
        course_info = {'course_id': e_c.id,
              'course_name': e_c.name,
              'type': e_c.type,
              'credit': e_c.credit,
              'period': e_c.period}
        classes = Class.query.filter_by(course_id=e_c.id).all()
        if len(classes)>0:
            for c in classes:
                re = {'course_info': course_info}
                re['class_id'] = c.id
                re['choose'] = c.choose
                re['last_people'] = c.max_people - len(Curricula_variable.query.filter_by(class_id=c.id).all())
                all_teachers = Teach.query.filter_by(class_id=c.id).all()
                re['instructor_name'] = []
                for teacher in all_teachers:
                    t = Instructor.query.filter_by(id=teacher.instructor_id).first()
                    re['instructor_name'].append(t.name)
                schs = Schedule.query.filter_by(class_id=c.id)
                re['classroom_id'] = schs.first().classroom_id
                re['section'] = schs.first().section
                re['day'] = []
                for sch in schs.all():
                    re['day'].append(sch.day)
                result.append(re)
    return jsonify(result)


@student.route('/stu_choice_class', methods=['PUT', 'GET'])
@login_required
def choice_class():

    class_id = request.data.get('class_id')
    if Curricula_variable.query.filter_by(student_id=current_user, class_id=class_id).first() is not None:
        return jsonify({'message': 'had choose'}), 403
    class_info = Class.query.filter_by(id=class_id).first()
    if class_info is None:
        return jsonify({'message': 'no class'}), 404
    # 该门课剩余人数
    last_people = class_info.max_people - len(Curricula_variable.query.filter_by(class_id=class_info.id).all())
    # 学生年级
    if ((datetime.year - current_user.year > 1)
            or (datetime.year - current_user == 1 and datetime.month > 9))and last_people > 0:
        new_choose = Curricula_variable(classes=class_info, student=current_user, grade=0)
        db.session.add(new_choose)
        db.session.commit()
        return jsonify({'message': 'choose successful'})
    else:
        return jsonify({'message': "can't choose "}), 403


@student.route('/exam,_info',methods=['GET'])
@login_required
def exam_info():
    my_exams = Take_exam.query.filter_by(student_id=current_user.id).all()
    if len(my_exams) == 0:
        return jsonify({'message': 'no exam'}), 404
    result = []
    for my_exam in my_exams:
        exam = {}
        exam_infos = Exam.query.filter_by(id=my_exam.exam_id).first()
        class_infos = Class.query.filter_by(id=my_exam.class_id).first()
        if exam_info is not None and class_infos is not None:
            exam['exam_grade'] = my_exam.exam_grade
            exam['classroom'] = exam_infos.exam_room
            exam['date'] = exam.date
            exam['time'] = exam.time
            exam['course_name'] = Course.query.filter_by(id=class_infos.course_id).first().name
            if exam['course_name'] is not None:
                result.append(exam)
    return jsonify(result)