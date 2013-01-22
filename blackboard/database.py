# -*- coding: utf-8 -*-

try:
    from flaskext.sqlalchemy import SQLAlchemy
except ImportError:
    from flask.ext.sqlalchemy import SQLAlchemy

from base import app
import config



app.config['SQLALCHEMY_DATABASE_URI'] = config.get('database_uri')
db = SQLAlchemy(app)


class Posts(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    content_type = db.Column(db.String(5))
    time = db.Column(db.DateTime)

    is_public = db.Column(db.Boolean)
    public_id = db.Column(db.String(6), unique=True)

    comments = db.relationship('Comments', backref='posts')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', backref='posts', uselist=False)


    def __init__(self, title, content, comment, content_type, time, user,
                 is_public, public_id):

        self.title = title
        self.content = content
        self.comment = comment
        self.content_type = content_type
        self.time = time
        self.user = user
        self.is_public = is_public
        self.public_id = public_id


class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)

    admin = db.Column(db.Boolean)
    active = db.Column(db.Boolean)

    last_login = db.Column(db.DateTime)
    posts_per_page = db.Column(db.Integer)
    email_notification = db.Column(db.Boolean)
    remember_me = db.Column(db.Boolean)
    template = db.Column(db.String(40))
    avatar = db.Column(db.String(80))
    facebook_integration = db.Column(db.Boolean)


    def __init__(self, name, password, email, admin, active, last_login,
                 posts_per_page, email_notification, remember_me, template,
                 avatar, facebook_integration):

        self.name = name
        self.password = password
        self.email = email
        self.admin = admin
        self.active = active
        self.last_login = last_login
        self.posts_per_page = posts_per_page
        self.email_notification = email_notification
        self.remember_me = remember_me
        self.template = template
        self.avatar = avatar
        self.facebook_integration = facebook_integration

class Comments(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)

    related_post = db.Column(db.Integer, db.ForeignKey('posts.id'))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', backref='comments', uselist=False)


    def __init__(self, content, time, related_post, user_id):

        self.content = content
        self.time = time
        self.related_post = related_post
        self.user_id = user_id

class Facebook(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    access_token = db.Column(db.Integer)
    expire_time = db.Column(db.DateTime)


    def __init__(self, user_id, access_token, expire_time):

        self.user_id = user_id
        self.access_token = access_token
        self.expire_time = expire_time

