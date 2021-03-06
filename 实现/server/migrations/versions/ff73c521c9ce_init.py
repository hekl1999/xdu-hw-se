"""init

Revision ID: ff73c521c9ce
Revises: 
Create Date: 2018-06-14 20:12:04.519022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff73c521c9ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('account', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(length=32), nullable=False),
    sa.Column('type', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('account')
    )
    op.create_index(op.f('ix_accounts_account'), 'accounts', ['account'], unique=True)
    op.create_table('admins',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admins_id'), 'admins', ['id'], unique=False)
    op.create_table('classrooms',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('building', sa.String(length=32), nullable=False),
    sa.Column('floor', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_classrooms_id'), 'classrooms', ['id'], unique=False)
    op.create_table('courses',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('type', sa.String(length=16), nullable=False),
    sa.Column('credit', sa.Integer(), nullable=False),
    sa.Column('period', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=True)
    op.create_index(op.f('ix_courses_name'), 'courses', ['name'], unique=False)
    op.create_index(op.f('ix_courses_type'), 'courses', ['type'], unique=False)
    op.create_table('instructors',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_instructors_id'), 'instructors', ['id'], unique=False)
    op.create_table('students',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_students_id'), 'students', ['id'], unique=True)
    op.create_table('superiors',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_superiors_id'), 'superiors', ['id'], unique=False)
    op.create_table('classes',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('term', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.String(length=64), nullable=True),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('max_people', sa.Integer(), nullable=False),
    sa.Column('optional', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_classes_id'), 'classes', ['id'], unique=False)
    op.create_table('curricula_variables',
    sa.Column('student_id', sa.String(length=32), nullable=False),
    sa.Column('class_id', sa.String(length=64), nullable=False),
    sa.Column('grade', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('student_id', 'class_id')
    )
    op.create_table('exams',
    sa.Column('id', sa.String(length=16), nullable=False),
    sa.Column('classes_id', sa.String(length=64), nullable=False),
    sa.Column('date', sa.String(length=64), nullable=False),
    sa.Column('time', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['classes_id'], ['classes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exams_id'), 'exams', ['id'], unique=False)
    op.create_table('schedules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.String(length=64), nullable=False),
    sa.Column('classroom_id', sa.String(length=32), nullable=False),
    sa.Column('week', sa.Integer(), nullable=False),
    sa.Column('day', sa.Integer(), nullable=False),
    sa.Column('section', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['classroom_id'], ['classrooms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teaches',
    sa.Column('instructor_id', sa.String(length=32), nullable=False),
    sa.Column('class_id', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['instructor_id'], ['instructors.id'], ),
    sa.PrimaryKeyConstraint('instructor_id', 'class_id')
    )
    op.create_table('exam_rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('exam_id', sa.String(length=16), nullable=False),
    sa.Column('classroom_id', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['classroom_id'], ['classrooms.id'], ),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exam_rooms_classroom_id'), 'exam_rooms', ['classroom_id'], unique=False)
    op.create_index(op.f('ix_exam_rooms_exam_id'), 'exam_rooms', ['exam_id'], unique=False)
    op.create_table('take_exams',
    sa.Column('exam_id', sa.String(length=16), nullable=False),
    sa.Column('student_id', sa.String(length=32), nullable=False),
    sa.Column('exam_grade', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('exam_id', 'student_id')
    )
    op.create_index(op.f('ix_take_exams_exam_id'), 'take_exams', ['exam_id'], unique=False)
    op.create_index(op.f('ix_take_exams_student_id'), 'take_exams', ['student_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_take_exams_student_id'), table_name='take_exams')
    op.drop_index(op.f('ix_take_exams_exam_id'), table_name='take_exams')
    op.drop_table('take_exams')
    op.drop_index(op.f('ix_exam_rooms_exam_id'), table_name='exam_rooms')
    op.drop_index(op.f('ix_exam_rooms_classroom_id'), table_name='exam_rooms')
    op.drop_table('exam_rooms')
    op.drop_table('teaches')
    op.drop_table('schedules')
    op.drop_index(op.f('ix_exams_id'), table_name='exams')
    op.drop_table('exams')
    op.drop_table('curricula_variables')
    op.drop_index(op.f('ix_classes_id'), table_name='classes')
    op.drop_table('classes')
    op.drop_index(op.f('ix_superiors_id'), table_name='superiors')
    op.drop_table('superiors')
    op.drop_index(op.f('ix_students_id'), table_name='students')
    op.drop_table('students')
    op.drop_index(op.f('ix_instructors_id'), table_name='instructors')
    op.drop_table('instructors')
    op.drop_index(op.f('ix_courses_type'), table_name='courses')
    op.drop_index(op.f('ix_courses_name'), table_name='courses')
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.drop_table('courses')
    op.drop_index(op.f('ix_classrooms_id'), table_name='classrooms')
    op.drop_table('classrooms')
    op.drop_index(op.f('ix_admins_id'), table_name='admins')
    op.drop_table('admins')
    op.drop_index(op.f('ix_accounts_account'), table_name='accounts')
    op.drop_table('accounts')
    # ### end Alembic commands ###
