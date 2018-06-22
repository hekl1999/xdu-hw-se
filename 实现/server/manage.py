from app import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
# from app.models import User, Picture,Role
from app.main import InsertData

app = create_app('testing')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db,InsertData=InsertData)


manager.add_command("shell", Shell(make_context=make_shell_context))


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0')
    manager.run()

