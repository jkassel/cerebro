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
    DEBUG_TB_ENABLED = True


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
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'
    DEBUG_TB_ENABLED = False