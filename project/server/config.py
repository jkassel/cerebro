# config.jinja2

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = '7d84ed5818d603c468af50dda9289f0f2af0c70c0ea753c1041a6635aef1dcb9'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    HOST = "0.0.0.0"


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
    DEBUG_TB_ENABLED = False


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    DEBUG_TB_ENABLED = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = '7d84ed5818d603c468af50dda9289f0f2af0c70c0ea753c1041a6635aef1dcb9'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://qhngbffpbuflsp:20614672c5f4d50fa1b731a6bed4e29f6e05f16e235129535f95ebc1a97d3363@ec2-184-73-240-228.compute-1.amazonaws.com:5432/da5slfsl8j6sf3'
    DEBUG_TB_ENABLED = False