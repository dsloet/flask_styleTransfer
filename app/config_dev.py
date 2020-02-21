import logging

from app.config_common import *

import os


# DEBUG can only be set to True in a development environment for security reasons
DEBUG = True

# Secret key for generating tokens
SECRET_KEY = 'houdini'

# Admin credentials
ADMIN_CREDENTIALS = ('admin', 'pa$$word')

# Database choice
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Configuration of a Gmail account for sending mails
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'flask.boilerplate'
MAIL_PASSWORD = 'flaskboilerplate123'
ADMINS = ['flask.boilerplate@gmail.com']

# Number of times a password is hashed
BCRYPT_LOG_ROUNDS = 12

LOG_LEVEL = logging.DEBUG
LOG_FILENAME = 'activity.log'
LOG_MAXBYTES = 1024
LOG_BACKUPS = 2

# Directories
UPLOAD_FOLDER = os.path.join("app", "static", "uploads")
THUMBNAIL_FOLDER = os.path.join("app", "static", "uploads", "thumpnails") #'static/uploads/thumpnails'
RESULT_FOLDER = os.path.join("app", "results")

# AWS
BUCKET = "styletransferbucketsloet"
S3_UPLOAD_FOLDER = "uploads"
