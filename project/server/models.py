# project/server/models.py


import datetime

from project.server import app, db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False, first_name="", last_name="", profile_status="private"):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

        self.first_name = db.Column(db.String(255), nullable=True)
        self.last_name = db.Column(db.String(255), nullable=True)
        self.profile_status = db.Column(db.String(255), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_profile_status(self):
        return self.profile_status

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class Idea(db.Model):

    __tablename__ = "ideas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    owner = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=True)

    # access types: public, private, team
    access = db.Column(db.String(255), nullable=False)

    def __init__(self, owner, title, access="private", description=""):
        self.owner = owner
        self.title = title
        self.description = description
        self.rating = 0
        self.access = access

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_rating(self):
        return self.rating

    def get_access(self):
        return self.access

    def __repr__(self):
        return '<Idea {0}'.format(self.title)


class UserProfile(db.Model):
    __tablename__ = "user_profile"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    user = db.Column(db.Integer, nullable=False)

    def __init__(self, user, first_name="", last_name=""):
        self.first_name = first_name
        self.last_name = last_name
        self.user = user


