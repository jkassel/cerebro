# project/server/models.py


import datetime

from project.server import app, db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    profile_status = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(db.String(1024), nullable=True)
    about_me = db.Column(db.String(1024), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    age = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(1024), nullable=True)
    facebook_url = db.Column(db.String(255), nullable=True)
    twitter_url = db.Column(db.String(255), nullable=True)

    def __init__(self, user_name,
                 email,
                 password,
                 admin=False,
                 first_name="",
                 last_name="",
                 profile_status="private",
                 profile_pic="https://s3.amazonaws.com/cerebro-kassellabs-data/public/default-user-image.png",
                 about_me="",
                 location="",
                 age=None,
                 website="#",
                 facebook_url="#",
                 twitter_url="#",
                 ):
        self.user_name = user_name
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.last_login = datetime.datetime.now()
        self.admin = admin

        self.first_name = first_name
        self.last_name = last_name
        self.profile_status = profile_status
        self.profile_pic = profile_pic
        self.about_me = about_me

        self.location = location
        self.age = age
        self.website = website
        self.facebook_url = facebook_url
        self.twitter_url = twitter_url

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

    def get_sign_up_date(self):
        return pretty_date(self.registered_on)

    def get_last_login(self):
        return pretty_date(self.last_login)

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class Idea(db.Model):

    __tablename__ = "ideas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    owner = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, nullable=False)

    # access types: public, private, team
    access = db.Column(db.String(255), nullable=False)

    def __init__(self, owner, title, access="private", description=""):
        self.owner = owner
        self.title = title
        self.description = description
        self.rating = 0
        self.access = access
        self.created_date = datetime.datetime.now()

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_rating(self):
        return self.rating

    def get_access(self):
        return self.access

    def get_created_date(self):
        return pretty_date(self.registered_on)

    def __repr__(self):
        return '<Idea {0}'.format(self.title)


class AuditLog(db.Model):

    __tablename__ = "audit_log"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    action = db.Column(db.String(255), nullable=False)
    resource = db.Column(db.String(255), nullable=False)

    def __init__(self, user, action, resource):

        # actions <resource>:
        #   login, logout
        #   created idea <idea>, updated idea <idea>, deleted idea <idea>
        #   added <user> to team
        #   updated profile
        #   started project on idea <idea>

        self.timestamp = datetime.datetime.now()
        self.user = user
        self.action = action
        self.resource = resource


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(int(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(int(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(int(day_diff / 30)) + " months ago"
    return str(int(day_diff / 365)) + " years ago"