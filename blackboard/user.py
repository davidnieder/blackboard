# -*- coding: UTF-8 -*-

from datetime import datetime
from flask.ext.login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

import exceptions
import config
from base import app
from database import db, Users as DBUsers



class User:

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

        if self.id:
            self.db_user = DBUsers.query.filter_by(id=self.id).first()
        elif self.name:
            self.db_user = DBUsers.query.filter_by(name=self.name).first()
        else:
            return

        if self.db_user:
            self.id = self.db_user.id
            self.name = self.db_user.name
            self.password = self.db_user.password
            self.email = self.db_user.email
            self.admin = self.db_user.admin
            self.active = self.db_user.active
            self.last_login = self.db_user.last_login
            self.posts_per_page = self.db_user.posts_per_page
            self.email_notification = self.db_user.email_notification
            self.remember_me = self.db_user.remember_me
            self.template = self.db_user.template
            self.avatar = self.db_user.avatar
            self.facebook_integration = self.db_user.facebook_integration
        else:
            self.id = None

    def update_setting(self, setting, value):
        if hasattr(self, setting):
            setattr(self, setting, value)
            setattr(self.db_user, setting, value)

            db.session.add(self.db_user)
            db.session.commit()

    def set_password(self, password):
        pw_hash = generate_password_hash(password)
        self.update_setting('password', pw_hash)

    def delete(self):
        db.session.delete(self.db_user)
        db.session.commit()

    # flaskext.login methods
    def authenticate(self, password):
        return True if check_password_hash(self.password, password) else False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True if self.active else False

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def login(self, remember=False):
        self.update_setting('last_login', datetime.utcnow())
        login_user(self, remember=remember)

    def logout(self):
        logout_user()


class NewUser(User):

    def __init__(self, name, password, email):
        User.__init__(self, name=name)

        if self.id:
            raise exceptions.UserAlreadyExists()

        else:
            # todo: validate this inputs

            self.name = name
            self.password = generate_password_hash(password)
            self.email = email

            # user defaults
            self.admin = False
            self.active = False if config.get('account_activation', bool) \
                                else True
            self.last_login = None
            self.posts_per_page = config.get('posts_per_page', int)
            self.email_notification = False
            self.remember_me = False
            self.template = 'default'
            self.avatar = None
            self.facebook_integration = False

    def create(self):
            self.db_user = DBUsers(
                            name = self.name,
                            password = self.password,
                            email = self.email,
                            admin = self.admin,
                            active = self.active,
                            last_login = self.last_login,
                            posts_per_page = self.posts_per_page,
                            email_notification = self.email_notification,
                            remember_me = self.remember_me,
                            template = self.template,
                            avatar = self.avatar,
                            facebook_integration = self.facebook_integration
                            )

            db.session.add(self.db_user)
            db.session.commit()

            self.id = self.db_user.id


def get(user_id):
    '''Returns User-object or None'''
    user = User(id=int(user_id))
    return user if user.id else None

def get_username_from_id(user_id):
    '''Returns corresponding user name or None'''
    user = User(id=int(user_id))
    return user.name if user.id else False

def get_user_id_from_name(username):
    '''Returns corresponding user id or None'''
    user = User(name=username)
    return user.id if user.id else None

def get_current_user():
    '''Returns the current, logged-in user or None'''
    if current_user.is_anonymous():
        return None
    else:
        return current_user

def get_current_db_user():
    '''Returns db object of the current user or None'''
    user = get_current_user()
    if user:
        return user.db_user
    else:
        return None

def current_user_is_admin():
    if current_user.is_anonymous():
        return False
    else:
        return True if current_user.admin else False

def get_posts_per_page():
    if current_user.is_anonymous():
        return config.get('posts_per_page', int)
    else:
        return current_user.posts_per_page

def get_template():
    if current_user.is_anonymous():
        return 'default'
    else:
        return current_user.template

def get_user_list():
    return DBUsers.query.all()

