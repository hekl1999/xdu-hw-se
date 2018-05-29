<<<<<<< HEAD
from flask import current_app, request, jsonify
from ..models import *
from flask_login import current_user, login_required
from .. import app, db
from . import teacher
import json

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


@teacher.route('/tea_insert_grade',methods=['PUT','POST'])
@login_required
def insert_grade():
    data = json.loads(request.data)
    class_id = data.get('class_id')
    if class_id is None:
        return jsonify({'message': 'no class_id'}), 403
    input_grades = data.get('grade')
    if input_grades is None or len(input_grades) == 0:
        return jsonify({'message': 'no grade'}), 403
    class_info = Class.query.filter_by(id=class_id).first()
    if class_info is None:
        return jsonify({'message': 'no class'}), 404
    if Teach.query.filter_by(class_id=class_id,instructor_id=current_user.id).first() is None:
        return jsonify({'message': 'not teach this class'}), 403
    all_students = Curricula_variable.query.filter_by(class_id=class_id).all()
    for grade_data in input_grades:
        bad_data = []
        try:
            student = Curricula_variable.query.filter_by(student_id=grade_data.get('student_id')).first()
            if student is None or student not in all_students:
                bad_data.append(grade_data.get('student_id'))
            else:
                student.grade = grade_data.get('grade')
                db.session.add(student)
        except:
            bad_data.append(grade_data.get('student_id'))
    db.session.commit()
    return jsonify(bad_data), 200


@teacher.route('/exam_info')
@login_required
def exam_info():
    my_teaches = Teach.query.filter_by(instructor_id=current_user.id).all()
    if len(my_teaches) > 0:
        result = []
        for my_teach in my_teaches:
            # 一门课可以安排多个时间考试
            exam_infos = Exam.query.filter_by(class_id=my_teach.class_id).all()
            for exam in exam_infos:
                re = {'date': exam.date,
                      'time': exam.time,
                      'course_name': my_teach.classes.course.name}
                exam_rooms = Exam_room.query.filter_by(exam_id=exam.id).all()
                re['classroom_id'] = [ex.classroom.id for ex in exam_rooms]
                result.append(re)
        return jsonify(result)
    else:
        return jsonify({'message': 'no data'}), 404
=======
from flask import current_app, request, jsonify, session
from ..models import *
from flask_login import current_user, login_required
from .. import app, db
from . import teacher
import json


@teacher.route('/mine_class')
@login_required
def mine_class():
    print(request.cookies)
    mine_teachs = Teach.query.filter_by(instructor_id=current_user.id).all()
    if len(mine_teachs) == 0:
        return jsonify({'message':'no class'}), 404
    result = []
    for mine_cla in mine_teachs:
        class_id = mine_cla.class_id
        re = {'class_id':class_id,
              'course_id':mine_cla.classes.course.id,
              'course_name':mine_cla.classes.course.name}
        sch = Schedule.query.filter_by(class_id=class_id).first()
        if sch is None:
            return jsonify({'message':'data missing'}), 404
        re['classroom_id'] = sch.classroom_id
        re['day'] = sch.day
        re['week'] = sch.week
        re['section'] = sch.section
        result.append(re)
    return jsonify(result)


@teacher.route('/class_info')
@login_required
def tea_class():
    tea_infos = Teach.query.all()
    print('cookies:')
    print(request.cookies)
    # print('cookies:')
    print(session)
    print(tea_infos)
    if len(tea_infos) == 0:
        return jsonify({'message': 'no class'}), 404
    else:
        result= []
        for tea_info in tea_infos:
            re = {'class_id': tea_info.classes.id,
                  'course_id': tea_info.classes.course.id,
                  'course_name': tea_info.classes.course.name,
                  'type': tea_info.classes.course.type}
            schs = Schedule.query.filter_by(class_id=tea_info.classes.id).all()
            re_time = [{'day': s.day, 'section': s.section} for s in schs]
            re['time'] = re_time
            result.append(re)
        print(result)
        return jsonify(result)


@teacher.route('/class_people', methods=['POST'])
@login_required
def class_info():
    class_id= request.form.get('class_id')
    if class_id is None:
        return jsonify({'message':'no data'}), 401
    teas = Teach.query.filter_by(class_id=class_id).all()
    if current_user.id not in [tea.teacher.id for tea in teas]:
        return jsonify({'message':'you are not its teacher'}), 403
    student_infos = CurriculaVariable.query.filter_by(class_id= class_id).all()
    result = []
    for student_info in student_infos:
        re = {'student_id':student_info.student.id,
              'student_name':student_info.student.name,
              'grade':student_info.grade}
        result.append(re)
    return jsonify(result)


@teacher.route('/insert_grade', methods=['PUT', 'POST'])
@login_required
def insert_grade():
    data = request.get_json()
    class_id = data.get('class_id')
    if class_id is None:
        return jsonify({'message': 'no class_id'}), 403
    input_grades = data.get('grade')
    if input_grades is None or len(input_grades) == 0:
        return jsonify({'message': 'no grade'}), 403
    class_info = Class.query.filter_by(id=class_id).first()
    if class_info is None:
        return jsonify({'message': 'no class'}), 404
    if Teach.query.filter_by(class_id=class_id, instructor_id=current_user.id).first() is None:
        return jsonify({'message': 'not teach this class'}), 403
    all_students = CurriculaVariable.query.filter_by(class_id=class_id).all()
    for grade_data in input_grades:
        bad_data = []
        try:
            student = CurriculaVariable.query.filter_by(student_id=grade_data.get('student_id')).first()
            if student is None or student not in all_students:
                bad_data.append(grade_data.get('student_id'))
            else:
                student.grade = grade_data.get('grade')
                db.session.add(student)
        except:
            bad_data.append(grade_data.get('student_id'))
    db.session.commit()
    return jsonify(bad_data), 200


@teacher.route('/exam_info')
@login_required
def exam_info():
    my_teaches = Teach.query.filter_by(instructor_id=current_user.id).all()
    if len(my_teaches) > 0:
        result = []
        for my_teach in my_teaches:
            # 一门课可以安排多个时间考试
            exam_infos = Exam.query.filter_by(classes_id=my_teach.class_id).all()
            for exam in exam_infos:
                re = {'date': exam.date,
                      'time': exam.time,
                      'course_name': my_teach.classes.course.name}
                exam_rooms = Exam_room.query.filter_by(exam_id=exam.id).all()
                re['classroom_id'] = [ex.classroom.id for ex in exam_rooms]
                result.append(re)
        return jsonify(result)
    else:
        return jsonify({'message': 'no data'}), 404
>>>>>>> b070cac5f8bb4dc4a6982e2d2961c68ee3f5514c
