# project/server/user/views.py


#################
#### imports ####
#################
import os
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user

from project.server import bcrypt, db, app
from project.server.models import User, Idea
from project.server.user.forms import LoginForm, RegisterForm, IdeaForm, ResetPasswordForm, UserProfileForm
import boto3
import sys
import datetime
from froala_editor import S3
import secrets

################
#### config ####
################

user_blueprint = Blueprint('user', __name__,)
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'

S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

s3_client = boto3.client('s3', aws_access_key_id=S3_KEY,
                         aws_secret_access_key=S3_SECRET)

################
#### routes ####
################


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():

        user = User(
            user_name=form.user_name.data,
            email=form.email.data,
            password=form.password.data
        )

        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Thank you for registering.', 'success')
        return redirect(url_for("user.ideas"))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(
                user.password.encode('utf-8'), request.form['password'].encode('utf-8')):
            login_user(user)
            current_user.last_login = datetime.datetime.now()
            db.session.commit()
            flash('You are logged in. Welcome!', 'success')
            return redirect(url_for('user.ideas'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', title='Please Login', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/members')
@login_required
def members():
    return render_template('user/members.html')


@user_blueprint.route('/ideas/create', methods=['GET', 'POST'])
def create_idea():
    form = IdeaForm(request.form)
    if form.validate_on_submit():
        owner = int(current_user.id)
        idea = Idea(owner=owner, title=form.title.data, description=form.description.data,
                    access=form.access.data)
        db.session.add(idea)
        db.session.commit()

        flash('Idea Added!', 'success')
        return redirect(url_for("user.my_ideas"))
    return render_template('user/create_idea.html', form=form)


@user_blueprint.route('/my_ideas', methods=['GET', 'POST'])
def my_ideas():
    owner_id = current_user.id
    idea_list = Idea.query.filter_by(owner=owner_id).all()
    return render_template('user/ideas.html', ideas=idea_list, title='My Ideas')


@user_blueprint.route('/ideas', methods=['GET', 'POST'])
def ideas():
    idea_list = Idea.query.filter_by(access='public')
    return render_template('user/ideas.html', ideas=idea_list, title='Ideas')


@user_blueprint.route('/ideas/<idea>/', methods=['GET', 'POST'])
def idea_detail(idea):
    idea_result = Idea.query.filter_by(id=idea).first()
    return render_template('user/idea_detail.html', idea=idea_result)


@user_blueprint.route('/ideas/<idea>/edit', methods=['GET', 'POST'])
def edit_idea(idea):
    idea_result = Idea.query.filter_by(id=idea).first()
    form = IdeaForm(request.form)
    if form.validate_on_submit():
        idea_result = Idea.query.filter_by(id=idea).first()
        idea_result.title = form.title.data
        idea_result.description = form.description.data
        idea_result.access = form.access.data
        db.session.commit()
        flash('Idea Updated!', 'success')
        return redirect(url_for("user.idea_detail", idea=idea))
    form.title.data = idea_result.title
    form.description.data = idea_result.description
    return render_template('user/idea_edit.html', idea=idea_result, form=form)


@user_blueprint.route('/resetpassword', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        user.password = bcrypt.generate_password_hash(
            form.password.data, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        db.session.commit()
        flash('Password Reset Successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('user/passwordreset.html', form=form)


@user_blueprint.route('/gethash', methods=['GET', 'POST'])
def get_s3_hash():
    config = {
        # The name of your bucket.
        'bucket': S3_BUCKET,

        # S3 region. If you are using the default us-east-1, it this can be ignored.
        'region': 'us-east-1',

        # The folder where to upload the images.

        'keyStart': current_user.email.split("@")[0] + "-" + str(current_user.id),

        # File access.
        'acl': 'public-read',

        # AWS keys.
        'accessKey': S3_KEY,
        'secretKey': S3_SECRET
    }

    try:
        response = S3.getHash(config)
        print("hash response: ", response)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return jsonify(**response)


@user_blueprint.route('/idea/delete/<idea>', methods=['GET', 'POST'])
def delete_idea(idea):
    owner = current_user.id
    Idea.query.filter_by(id=idea, owner=owner).delete()
    db.session.commit()
    flash('Idea Removed!', 'danger')
    return redirect(url_for("user.ideas"))


@user_blueprint.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UserProfileForm()
    if form.validate_on_submit():

        if form.profile_pic.data:
            picture_url = save_picture(form.profile_pic.data)
            current_user.profile_pic = picture_url
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.location = form.location.data
        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        current_user.age = form.age.data
        current_user.website = form.website.data
        current_user.facebook_url = form.facebook_url.data
        current_user.twitter_url = form.twitter_url.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash('Account Updated!', 'success')
        return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email
        form.location.data = current_user.location
        form.age.data = current_user.age
        form.website.data = current_user.website
        form.facebook_url.data = current_user.facebook_url
        form.twitter_url.data = current_user.twitter_url
        form.about_me.data = current_user.about_me
    username = current_user.id
    user = User.query.filter_by(id=username).first_or_404()
    user_ideas = Idea.query.filter_by(owner=user.id).all()
    return render_template('user/account.html', user=user, ideas=user_ideas, form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)

    picture_filename = random_hex + f_ext
    file_prefix = current_user.user_name + str(current_user.id)
    full_filename = "public/" + file_prefix + "/" + picture_filename
    bucket = S3_BUCKET
    try:
        s3_client.upload_fileobj(
            form_picture,
            bucket,
            full_filename,
            ExtraArgs={
                "ACL": 'public-read',
                "ContentType": form_picture.content_type
            }
        )
    except Exception as e:
        print("Error saving picture: ", e)

    picture_url = "https://s3.amazonaws.com/" + bucket + "/" + full_filename
    return picture_url

