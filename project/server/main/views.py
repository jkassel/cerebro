# project/server/main/views.py
import os

#################
#### imports ####
#################

from flask import render_template, Blueprint
from project.server import app


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################


@main_blueprint.route('/')
def home():
    #env = os.environ['APP_SETTINGS']
    env = app.config.get('APP_SETTINGS')
    return render_template('main/home.html', environment=env)


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")
