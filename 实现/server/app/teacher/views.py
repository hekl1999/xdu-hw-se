from flask import current_app, request, jsonify, session
from ..models import *
from flask_login import current_user, login_required
from .. import app, db
from . import teacher
import json


@teacher.route('/mine_class')
@login_required
def mine_class():
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
    mine_teachs = Teach.query.filter_by(instructor_id=current_user.id).all()
    schs = Schedule.query.filter(Schedule.class_id.in_([tea.class_id for tea in mine_teachs]))
    if len(mine_teachs) == 0:
        return jsonify({'message': 'no class'}), 404
    result = []
    temp_re = {}
    for mine_cla in mine_teachs:
        mine_cla =mine_cla.classes
        class_id = mine_cla.id
        temp_re[class_id] = {
            'class_id': class_id,
            'course_id': mine_cla.course.id,
            'course_name': mine_cla.course.name,
            'type': mine_cla.course.type,
            'classroom_id': [],
            'time': []
        }
    for sch in schs:
        temp_re[sch.class_id]['classroom_id'].append(sch.classroom_id)
        temp_re[sch.class_id]['time'].append({'day':sch.day,'section':sch.section})
    for keys in temp_re.keys():
        result.append(temp_re[keys])
    return jsonify(result)


@teacher.route('/class_people/<class_id>', methods=['GET'])
@login_required
def class_info(class_id):
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


@teacher.route('/insert_grade', methods=['POST', 'GET'])
@login_required
def insert_grade():
    data = json.loads(request.data.decode())
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
    for grade_data in input_grades:
        bad_data = []
        try:
            student = CurriculaVariable.query.filter_by(
                student_id=grade_data.get('student_id'), class_id=class_id).first()
            print(student.student_id, student.grade)
            if student is None :
                bad_data.append(grade_data.get('student_id'))
            else:
                student.grade = grade_data.get('grade')
                print(student.grade)
                db.session.add(student)
                db.session.commit()
        except:
            bad_data.append(grade_data.get('student_id'))
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

