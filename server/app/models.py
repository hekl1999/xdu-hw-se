from . import db, app, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from datetime import datetime


# 账户表
class Account(UserMixin, AnonymousUserMixin, db.Model):
    __tablename__ = 'accounts'
    account = db.Column(
        db.String(32),
        unique=True,
        primary_key=True,
        nullable=False,
        index=True)
    password = db.Column(db.String(32), nullable=False)
    type = db.Column(db.String(16), nullable=False)


@login_manager.user_loader
def load_user(account):
    account = Account.query.get(int(account))
    if account.type == 'student':
        return Student.query.get(int(account))
    elif account.type == 'instructor':
        return Instructor.query.get(int(account))
    elif account.type == 'leader':
        return Superior.query.get(int(account))
    elif account.type == 'Admin':
        return Admin.query.get(int(account))
    elif account in app.config['FLASKY_ADMIN']:
        return account


class AnonymousUser(AnonymousUserMixin):
    def can(self):
        return False

    def is_admin(self):
        return False


# 学生选课的表
class Curricula_variable(db.Model):
    __tablename__ = 'curricula_variables'
    student_id = db.Column(
        db.String(32),
        db.ForeignKey('students.id'),
        nullable=False,
        primary_key=True)
    class_id = db.Column(
        db.String(64),
        db.ForeignKey('classes.id'),
        nullable=False,
        primary_key=True)
    grade = db.Column(db.Integer)





# 教学表
class Teach(db.Model):
    __tablename__ = 'teaches'
    instructor_id = db.Column(
        db.String(32),
        db.ForeignKey('instructors.id'),
        nullable=False,
        primary_key=True)
    class_id = db.Column(
        db.String(64),
        db.ForeignKey('classes.id'),
        nullable=False,
        primary_key=True)


# 课程安排表
class Schedule(db.Model):
    __tablename__ = 'schedules'
    class_id = db.Column(
        db.String(64),
        db.ForeignKey('classes.id'),
        nullable=False,
        primary_key=True)
    classroom_id = db.Column(
        db.String(32),
        db.ForeignKey('classrooms.id'),
        nullable=False,
        primary_key=True)
    week = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    section = db.Column(db.Integer, nullable=False)


# 考场安排表
class Exam_room(db.Model):
    __tablename__ = 'exam_rooms'
    exam_id = db.Column(
        db.String(16),
        db.ForeignKey('exams.id'),
        nullable=False,
        primary_key=True,
        index=True)
    classroom_id = db.Column(
        db.String(32),
        db.ForeignKey('classrooms.id'),
        nullable=False,
        primary_key=True,
        index=True)


# 考试成绩表
class Take_exam(db.Model):
    __tablename__ = 'take_exams'
    exam_id = db.Column(
        db.String(16),
        db.ForeignKey('exams.id'),
        nullable=False,
        primary_key=True,
        index=True)
    student_id = db.Column(
        db.String(32),
        db.ForeignKey('students.id'),
        nullable=False,
        primary_key=True,
        index=True)
    exam_grade = db.Column(db.Integer)

# 学生表


class Student(db.Model, UserMixin, AnonymousUserMixin):
    __tablename__ = 'students'
    id = db.Column(
        db.String(32),
        unique=True,
        primary_key=True,
        nullable=False,
        index=True)
    name = db.Column(db.String(32), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    curricula_student = db.relationship(
        'Curricula_variable',
        foreign_keys=[
            Curricula_variable.student_id],
        backref=db.backref(
            'student',
            lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    exam_student = db.relationship(
        'Take_exam',
        foreign_keys=[
            Take_exam.student_id],
        backref=db.backref(
            'student',
            lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    # 学生当前的年级
    def grade(self):
        return datetime.now().year - self.year


# 教师表
class Instructor(db.Model, UserMixin, AnonymousUserMixin):
    __tablename__ = 'instructors'
    id = db.Column(db.String(32), primary_key=True, nullable=False, index=True)
    name = db.Column(db.String(32), nullable=False)
    teach_teacher = db.relationship(
        'Teach',
        foreign_keys=[Teach.instructor_id],
        backref=db.backref('teacher', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )


# 领导表

class Superior(db.Model, UserMixin, AnonymousUserMixin):
    __tablename__ = 'superiors'
    id = db.Column(db.String(32), primary_key=True, nullable=False, index=True)
    name = db.Column(db.String(32), nullable=False)


# 管理员
class Admin(db.Model, UserMixin, AnonymousUserMixin):
    __tablename__ = 'admins'
    id = db.Column(db.String(32), primary_key=True, nullable=False, index=True)
    name = db.Column(db.String(32), nullable=False)

# 课程表


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(
        db.String(32),
        primary_key=True,
        nullable=False,
        index=True,
        unique=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False, index=True)
    credit = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    classes = db.relationship('Class', backref='course', lazy='dynamic')


# 教室
class Classroom(db.Model):
    __tablename__ = 'classrooms'
    id = db.Column(db.String(32), primary_key=True, nullable=False, index=True)
    building = db.Column(db.String(32), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    schedule_classroom = db.relationship(
        'Schedule',
        foreign_keys=[
            Schedule.classroom_id],
        backref=db.backref(
            'classroom',
            lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    exam_classroom = db.relationship(
        'Exam_room',
        foreign_keys=[
            Exam_room.classroom_id],
        backref=db.backref(
            'classroom',
            lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

# 教学班表


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.String(64), primary_key=True, index=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    term = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.String(64), db.ForeignKey('courses.id'))
    number = db.Column(db.Integer, nullable=False)
    max_people = db.Column(db.Integer, nullable=False)  # 最大可选人数
    exam = db.relationship('Exam', backref='class', lazy='dynamic')
    choose = db.Column(db.Boolean)  # 课程是否可选
    curricula_class = db.relationship(
        'Curricula_variable',
        foreign_keys=[
            Curricula_variable.class_id],
        backref=db.backref(
            'class',
            lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    teach_class = db.relationship('Teach',
                                  foreign_keys=[Teach.class_id],
                                  backref=db.backref('class', lazy='joined'),
                                  lazy='dynamic',
                                  cascade='all, delete-orphan')
    schedule_class = db.relationship(
        'Schedule',
        foreign_keys=[
            Schedule.class_id],
        backref=db.backref(
            'class',
            lazy='joined'),
        lazy='dynamic',
        cascade='all,delete-orphan')


# 考试表
class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.String(16), primary_key=True, index=True)
    class_id = db.Column(
        db.String(64),
        db.ForeignKey('classes.id'),
        nullable=False)
    date = db.Column(db.String(64), nullable=False)  # 日期 格式为 年/月/日
    time = db.Column(db.String(64), nullable=False)   # 时间 格式为24小时制 hour:minute
    exam_room = db.relationship('Exam_room',
                                foreign_keys=[Exam_room.exam_id],
                                backref=db.backref('exam', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    exam_stu = db.relationship('Take_exam',
                               foreign_keys=[Take_exam.exam_id],
                               backref=db.backref('exam', lazy='joined'),
                               lazy='dynamic',
                               cascade='all,delete-orphan')
