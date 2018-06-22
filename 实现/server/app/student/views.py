from . import student
from .. import db, login_manager
from ..models import *
from flask import request, jsonify
from flask_login import current_user, login_required,login_manager
from datetime import datetime
login_manager.login_view = 'main.no_login'


@student.route('/mine_class', methods=['GET'])
@login_required
def mine_class():
    result = []
    my_classes = CurriculaVariable.query.filter_by(student_id=current_user.id).all()
    if len(my_classes) > 0:
        schs = Schedule.query.filter(Schedule.class_id.in_([c.class_id for c in my_classes])).all()
        teas = Teach.query.filter(Teach.class_id.in_([c.class_id for c in my_classes])).all()
        for (sch, tea) in [(sch, tea) for sch in schs
                            for tea in teas]:
            if sch.class_id == tea.class_id:
                re = {'course_id': sch.classes.course.id,
                      'course_name': sch.classes.course.name,
                      'instructor_name': [instructor.teacher.name for instructor in teas],
                      'classroom_id': sch.classroom_id,
                      'week': sch.week,
                      'day': sch.day,
                      'section': sch.section}
                result.append(re)
        return jsonify(result)
    return jsonify({'message': 'no course'}), 404


@student.route('/mine_grade', methods=['GET'])
@login_required
def mine_grade():
    result=[]
    my_classes = CurriculaVariable.query.filter_by(student_id=current_user.id).all()
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


@student.route('/class_list', methods=['GET'])
@login_required
def class_list():
    elective_courses = Course.query.filter(type != '1').all()
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
        if len(classes) > 0:
            for c in classes:
                re = {'course_info': course_info}
                re['class_id'] = c.id
                re['choose'] = c.optional
                re['select'] = (CurriculaVariable.query.filter_by(
                                student_id=current_user.id, class_id=c.id).first() is not None)
                re['last_people'] = c.max_people - len(CurriculaVariable.query.filter_by(class_id=c.id).all())
                all_teachers = Teach.query.filter_by(class_id=c.id).all()
                re['instructor_name'] = []
                for teacher in all_teachers:
                    t = Instructor.query.filter_by(id=teacher.instructor_id).first()
                    re['instructor_name'].append(t.name)
                schs = Schedule.query.filter_by(class_id=c.id)
                if schs.first() is not None:
                    re['classroom_id'] = schs.first().classroom_id
                    re['time'] = []
                    for sch in schs.all():
                        re['time'].append({'section': sch.section, 'day': sch.day})
                    result.append(re)
                else:
                    re['classroom_id'] = ''
                    re['time'] = []
    return jsonify(result)


@student.route('/choice_class/<class_id>', methods=['POST', 'GET'])
@login_required
def choice_class(class_id):
    course = CurriculaVariable.query.filter_by(student_id=current_user.id, class_id=class_id).first()
    # 取消选课
    if course is not None:
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "had cancel"})
    class_info = Class.query.filter_by(id=class_id).first()
    if class_info is None:
        return jsonify({'message': 'no class'}), 404
    # 该门课剩余人数
    last_people = class_info.max_people - len(CurriculaVariable.query.filter_by(class_id=class_info.id).all())
    # 学生年级
    if ((datetime.now().year - current_user.year > 1)
            or (datetime.year - current_user == 1 and datetime.month > 9))and last_people > 0:
        new_choose = CurriculaVariable(classes=class_info, student=current_user, grade=-1)
        db.session.add(new_choose)
        db.session.commit()
        return jsonify({'message': 'choose successful'})
    else:
        return jsonify({'message': "can't choose "}), 403


@student.route('/exam_info', methods=['GET'])
@login_required
def exam_info():
    my_exams = Take_exam.query.filter_by(student_id=current_user.id).all()
    if len(my_exams) == 0:
        return jsonify({'message': 'no exam'}), 404
    result = []
    all_exam = [exam.exam_id for exam in my_exams]
    exam_infoes = Exam.query.filter(Exam.id.in_(all_exam)).all()
    class_infos = Class.query.filter(Class.id.in_([exam.classes_id for exam in exam_infoes])).all()
    for (exam_infos,class_info) in [(exam_infos, class_info)
                                             for exam_infos in exam_infoes
                                             for class_info in class_infos]:
        if class_info.id == exam_infos.classes_id:
            re = {
                    'classroom_id': exam_infos.id,
                    'course_name': class_info.course.name,
                    'date': exam_infos.date,
                    'time': exam_infos.time
                  }
            result.append(re)
    return jsonify(result)


@student.route('/test_blueprint')
def student_test():
    return 'hello world'

