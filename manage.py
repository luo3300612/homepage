#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import random

COV = None
import coverage

if os.environ.get('FLASK_COVERAGE'):
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def rebuild():
    """Rebuild the project"""
    db.drop_all()
    db.create_all()
    Role.insert_roles()
    user1 = User(username='luo3300612', password="3300612", email='591486669@qq.com', location="Nanjing",
                 about_me="handsome", role_id=2)
    user2 = User(username='luo', password="3300612", email='john@example.com', location="Beijing", about_me="handsome",
                 role_id=3)
    db.session.add_all([user1, user2])
    db.session.commit()
    User.generate_fake(100)
    Post.generate_fake(100)
    users = User.query.all()
    for user in users:
        if random.randint(0, 1) == 1:
            user.follow(user1)
        else:
            user.follow(user2)
    db.session.commit()

@manager.command
def deploy():
    from flask_migrate import upgrade

    upgrade()

    Role.insert_roles()


@manager.command
def profile(length=25, profile_dir=None):
    """Start the app user the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


if __name__ == '__main__':
    manager.run()
