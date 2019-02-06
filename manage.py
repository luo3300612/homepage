#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role,Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


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


if __name__ == '__main__':
    manager.run()
