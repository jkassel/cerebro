# manage.py


import os
import unittest
import coverage
import random
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand


COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()

from project.server import app, db
from project.server.models import User, Idea


migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(email='ad@min.com', password='admin', admin=True))
    db.session.commit()


@manager.command
def create_users():
    db.session.add(User(
        user_name="jkassel",
        email="jkassel@gmail.com",
        first_name="Jeff",
        last_name="Kassel",
        location="Staten Island, NY",
        website="http://kassellabs.com",
        age=36,
        password="Password12!",
        about_me="Some stuff about me"
    ))

    db.session.add(User(
        user_name="jsmith",
        email="jsmith@jsmith.com",
        first_name="John",
        last_name="Smith",
        location="Orlando, FL",
        website="http://jsmith.com",
        age=36,
        password="Password12!",
        about_me="Some stuff about me"
    ))

    db.session.add(User(
        user_name="mjordan",
        email="michael@jordan.com",
        first_name="Michael",
        last_name="Jordan",
        location="Charlotte, NC",
        website="http://michaeljordan.com",
        age=56,
        password="Password12!",
        about_me="I like basketball"
    ))

    db.session.add(User(
        user_name="mtyson",
        email="mike@tyson.com",
        first_name="Mike",
        last_name="Tyson",
        location="Brooklyn, NY",
        website="http://miketyson.com",
        age=56,
        password="Password12!",
        about_me="I like to hit people"
    ))

    db.session.commit()
    print("Users created.")


@manager.command
def create_data():

    users = User.query.all()
    for user in users:
        for x in range(60):
            access_list = ['public', 'private']
            db.session.add(Idea(
                title="idea" + str(x),
                description="this is a test idea",
                owner=user.id,
                access=random.choice(access_list)
            ))
    db.session.commit()


port = int(os.environ.get('PORT', 5000))
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port=port))

if __name__ == '__main__':
    manager.run()
