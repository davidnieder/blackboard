# -*- coding: UTF-8 -*-

from flask import Flask
from flaskext.login import LoginManager

app = Flask(__name__)
app.config.from_object('blackboard.config-flask')

import database
import user
import urls
from config import LOGINREQUIREDMESSAGE

# Flask-Extension: LoginManager
loginmanager = LoginManager()
loginmanager.setup_app(app)
loginmanager.login_view = 'login'
loginmanager.login_message = LOGINREQUIREDMESSAGE
loginmanager.session_protection = 'strong'


@app.before_request
def before_reqeust():
    database.opendb()    

@app.teardown_request
def teardown_request(exception):
    database.closedb()

@loginmanager.user_loader
def load_user(userid):
    return user.get(userid)

