# -*- coding: UTF-8 -*-

from flask import Flask, g
from flaskext.login import LoginManager

app = Flask('blackboard')
app.config.from_object('blackboard.config-flask')

import database
import user
import urls
from config import LOGINREQUIREDMESSAGE, FEEDBACKADRESS, IMPRINTURI
from upload import initializeUpload

# Flask-Extension: LoginManager
loginmanager = LoginManager()
loginmanager.setup_app(app)
loginmanager.login_view = 'login'
loginmanager.login_message = LOGINREQUIREDMESSAGE
loginmanager.session_protection = 'strong'

# Flask-Extension: Uploads
imageUploadSet = initializeUpload('images')
fileUploadSet = initializeUpload('files')
avatarUploadSet = initializeUpload('avatars')
audioUploadSet = initializeUpload('audio')


@app.before_request
def before_reqeust():
    database.opendb()    

    # make this constants available globally
    g.FEEDBACKADRESS = FEEDBACKADRESS
    g.IMPRINTURI = IMPRINTURI


@app.teardown_request
def teardown_request(exception):
    database.closedb()

@loginmanager.user_loader
def load_user(userid):
    return user.get(userid)

if __name__ == '__main__':
    app.run()

