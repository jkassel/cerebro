# project/server/user/forms.py

from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SelectField, IntegerField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms.widgets import TextArea
from project.server.models import User


class LoginForm(FlaskForm):
    email = StringField('Email Address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])


class RegisterForm(FlaskForm):

    def validate_username(self, user_name):
        user = User.query.filter_by(username=user_name.data).first()
        if user:
            raise ValidationError('That username taken.  Please choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email in use by another account.  Please choose another.')

    user_name = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=24)])
    email = StringField(
        'Email Address',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )


class IdeaForm(FlaskForm):
    title = StringField('Title')
    description = StringField('Description', widget=TextArea())
    access = SelectField('Access', choices=[("public", "Public"), ("private", "Private")], default="private")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'New Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )


class UserProfileForm(FlaskForm):
    first_name = StringField('')
    last_name = StringField('')
    user_name = StringField('', validators=[DataRequired(), Length(min=3, max=24)])
    profile_pic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    def validate_username(self, user_name):
        if user_name.data != current_user.user_name:
            user = User.query.filter_by(username=user_name.data).first()
            if user:
                raise ValidationError('That username taken.  Please choose another.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email in use by another account.  Please choose another.')

    email = StringField('', validators=[DataRequired(), Email()])
    location = StringField('')
    age = IntegerField('', [validators.optional()])
    website = StringField('')
    facebook_url = StringField('')
    twitter_url = StringField('')
    about_me = StringField('', widget=TextArea())

