# -*- coding: utf-8 -*-

import random
import string
import datetime

from flask import Flask, session, request, abort
from flask.ext.login import LoginManager

import config

app = Flask(__name__)
app.config['DEBUG'] = config.get('debug', bool)
app.config['SECRET_KEY'] = config.get('secret_key')
app.config['REMEMBER_COOKIE_NAME'] = config.get('remember_cookie_name')
app.config['REMEMBER_COOKIE_DURATION'] = datetime.timedelta(days=
    config.get('remember_cookie_duration', int))


import urls
import user
import messages
from upload import initializeUpload

# Flask-Extension: Uploads
imageUploadSet = initializeUpload('images')
audioUploadSet = initializeUpload('audio')

# Flask-Extension: Login
loginmanager = LoginManager()
loginmanager.setup_app(app)
loginmanager.login_view = 'login'
loginmanager.login_message = messages.login_required
loginmanager.session_protection = 'strong'

@loginmanager.user_loader
def load_user(userid):
    return user.get(userid)

# csrf protection
@app.before_request
def csrf_protection():
    if request.method == 'POST':
        token = session.pop('csrf_token', None)
        if not token or token != request.form.get('csrf_token'):
            abort(403)

def generate_csrf_token():
    if 'csrf_token' not in session:
        rs = ''.join(random.choice(string.uppercase+string.digits) \
             for x in range(24))
        session['csrf_token'] = rs
    return session['csrf_token']

# jinja2 environment
app.jinja_env.filters['len'] = lambda(obj):len(obj)
app.jinja_env.filters['date'] = lambda(dt_obj):dt_obj.strftime('%B %d, %Y') \
                                if hasattr(dt_obj, 'strftime') else dt_obj
app.jinja_env.filters['time'] = lambda(dt_obj):dt_obj.strftime('%H:%M') \
                                if hasattr(dt_obj, 'strftime') else dt_obj
app.jinja_env.filters['date_and_time'] = lambda(dt_obj):dt_obj.strftime \
                                         ('%d.%m.%y %H:%M') if hasattr(dt_obj,
                                         'strftime') else dt_obj
app.jinja_env.filters['db_format'] = lambda(dt_obj):dt_obj.strftime('%Y-%m-%d') \
                                     if hasattr(dt_obj, 'strftime') else dt_obj
 
app.jinja_env.globals['csrf_token'] = generate_csrf_token
app.jinja_env.globals['IMPRINT_URI'] = config.get('imprint_uri')
app.jinja_env.globals['FEEDBACK_ADDRESS'] = config.get('feedback_address')

# setup
@app.before_request
def run_setup():
    if config.get('setup', bool):
        import setup
        return setup.setup()

