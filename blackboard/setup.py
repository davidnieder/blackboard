# -*- coding: utf-8 -*-

import os

from sqlalchemy.exc import ArgumentError
from sqlalchemy.engine.url import _parse_rfc1738_args

from flask import abort, request, redirect, render_template, url_for, flash

from base import app
from database import db
from user import NewUser
import config
import urls
import messages


def setup():
    if not config.get('setup', bool):
        abort(404)

    if request.method == 'POST':
        if not check_keys():
            flash(error_message)
            return render_template('setup.html')

        username = request.form['username']
        password = request.form['password_1']
        email = request.form['email']
        db_uri = request.form['database_uri']

        # create database
        config.set('database_uri', db_uri)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        db.drop_all()
        db.create_all()

        # create admin user
        admin = NewUser(username, password, email)
        admin.admin = True
        admin.active = True
        admin.create()

        # generate secret key
        secret_key = os.urandom(24)
        config.set('secret_key', secret_key)
        app.config['SECRET_KEY'] = secret_key

        # set a default upload directory
        blackboard_root = os.path.dirname(os.path.abspath(__file__))
        config.set('upload_destination', blackboard_root + '/static/upload')

        # disable setup
        config.set('setup', 'False')

        flash(messages.setup_finished, 'message')
        return redirect(url_for('login'))    

    else:
        return render_template('setup.html')

def check_keys():
    global error_message

    if request.form.get('database_uri') and request.form.get('username') and \
       request.form.get('password_1') and request.form.get('password_2') and \
       request.form.get('email'):

        try:
            _parse_rfc1738_args(request.form.get('database_uri'))
        except ArgumentError:
            error_message = messages.invalid_database_uri
            return False

        if request.form['password_1'] != request.form['password_2']:
            error_message = messages.passwords_dont_match
            return False

        return True

    else:
        error_message = u'Please fill in all fields'
        return False    

