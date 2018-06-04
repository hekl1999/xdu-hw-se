from .. import app,db
from flask import request,jsonify
from flask_login import login_required,current_user
from . import root
from ..models import *


@root.route('/root_show_tables')
@login_required
def root_show_table():
    table_name = [table for table in db.get_tables_for_bind()]
    return jsonify(table_name)


@root.route('/root_get_table')
@login_required
def root_get_table():
    table_dict = {}
    for table in db.get_tables_for_bind():
        table_dict[table.name] = table
    # table_name to models
    table_name_models = {
        'accounts': Account,
        'curriculaVariables':CurriculaVariable,
        'teaches':Teach,
        'schedules':Schedule,
        'exam_rooms':Exam_room,
        'take_exam':Take_exam,
        'students':Student,
        'instructors':Instructor,
        'superiors':Superior,
        'admins':Admin,
        'courses':Course,
        'classrooms':Classroom,
        'classes':Class,
        'exams':Exam
    }
    tablename = request.form.get('table_name')
    if tablename not in table_name_models.keys() or tablename is None:
        return jsonify({'message':'data error'}), 403
    result = {'format':[col.name for col in table_dict[tablename].columns]}
    all_datas = table_name_models[tablename].query.all()
    data = []
    for row_data in all_datas:
        data.append(row_data.show())
    result['data'] = data
    return jsonify(result)