# project/server/user/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from project.server import bcrypt, db
from project.server.models import User, Idea
from project.server.user.forms import LoginForm, RegisterForm, IdeaForm

################
#### config ####
################

user_blueprint = Blueprint('user', __name__,)


################
#### routes ####
################

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
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
                user.password, request.form['password']):
            login_user(user)
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
    print("form: " + str(form))
    if form.validate_on_submit():
        owner = int(current_user.id)
        print("form owner: " + str(owner))
        print("form title: " + str(form.title.data))
        idea = Idea(owner=owner, title=form.title.data, description=form.description.data)
        print("idea to add: " + str(idea))
        db.session.add(idea)
        db.session.commit()

        flash('Idea Added!', 'success')
        return redirect(url_for("user.ideas"))
    return render_template('user/create_idea.html', form=form)


@user_blueprint.route('/ideas', methods=['GET', 'POST'])
def ideas():
    owner_id = current_user.id
    print("owner Id: " + str(owner_id))
    print("got here")
    idea_list = Idea.query.filter_by(owner=owner_id).all()
    print(idea_list)
    return render_template('user/ideas.html', ideas=idea_list)


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
        db.session.commit()
        flash('Idea Updated!', 'success')
        return redirect(url_for("user.idea_detail", idea=idea))
    form.title.data = idea_result.title
    form.description.data = idea_result.description
    return render_template('user/idea_edit.html', idea=idea_result, form=form)



