# -*- coding: utf-8 -*-

from flask import render_template, url_for, flash, redirect, request, abort
from flask.ext.login import current_user

import config
import messages
from base import app
from user import User, get_user_list
from post import Post
from comment import Comment


def for_admin_only(f):
    def wrapper(*args, **kwargs):
        if current_user.is_admin():
            return f(*args, **kwargs)
        else:
            flash(messages.no_admin_access, 'error')
            return redirect(url_for('index'))
    return wrapper

@for_admin_only
def index():
    return render_template('admin/base.html')

@for_admin_only
def settings():
    if request.method == 'POST':
        setting = request.form.get('setting')
        value = request.form.get('value_0')
        # strip whitespaces
        value = value.replace(' ', '')
        if not setting or not value:
            abort(400)
        
        if setting not in config.options():
            abort(400)

        config.set(setting, value)
        return redirect(url_for('admin_settings'))

    # load settings
    setting_list = [
        'facebook_integration', 'facebook_app_id', 'facebook_app_secret',
        'feedback_address', 'imprint_uri', 'account_activation',
        'posts_per_page', 'templates', 'default_template', 'debug',
        'setup', 'file_extensions', 'max_file_size', 'registration',
        'posts_per_page_options', 'upload_destination'
    ]
    settings = {}
    for setting in setting_list:
        settings[setting] = config.get(setting)

    return render_template('admin/settings.html', settings=settings)

@for_admin_only
def user():
    if request.method == 'POST':
        setting = request.form.get('setting')
        user_id = request.form.get('value_0')
        value   = request.form.get('value_1')

        if not setting or not user_id:
            abort(400)
        try:
            user_id = int(user_id)
        except:
            abort(400)

        user = User(id=user_id)
        if not user.id:
            flash(messages.user_not_found)
            return render_template('admin/user.html',
                                   user_list=get_user_list())

        if setting == 'password':
            if not value:
                abort(400)

            user.set_password(value)
            flash(messages.user_set_password)

        elif setting == 'delete':
            user.delete()
            flash(messages.user_deleted)
            return redirect(url_for('admin_user'))

        elif setting == 'activate':
            if not value:
                abort(400)
            if value == 'True':
                user.update_setting('active', True)
                flash(messages.user_activated)
            else:
                user.update_setting('active', False)
                flash(messages.user_deactivated)

            return redirect(url_for('admin_user_details', id=user.id))

        else:
            abort(400)

    users = get_user_list()
    return render_template('admin/user.html', user_list=users)

@for_admin_only
def user_details(id):
    user = User(id=id)
    if not user.id:
        user = None

    return render_template('admin/user_details.html', user=user)

@for_admin_only
def post(id=None):
    if request.method == 'POST':
        setting = request.form.get('setting')
        post_id = request.form.get('value_0')
        value = request.form.get('value_1')

        if not setting or not post_id:
            abort(400)
        try:
            post_id = int(post_id)
        except:
            abort(400)

        post = Post(post_id=post_id)

        if not post.id:
            abort(400)

        if setting == 'delete':
            post.delete()
            flash(messages.post_deleted)

            if request.form.get('next'):
                return redirect(request.form['next'])
            return redirect(url_for('admin_post'))

        elif setting == 'public':
            if not value:
                abort(400)

            if value == 'True':
                post.set_public()
                flash(messages.post_marked_public)
            else:
                post.update('is_public', False)
                flash(messages.post_marked_private)

        return redirect(url_for('admin_post_id', id=post_id))

    else:
        if id:
            post = Post(post_id=id)
            post = post.get_post()

            if not post:
                flash(messages.post_not_found)
        else:
            post = None

        return render_template('admin/post.html', post=post)

@for_admin_only
def comment(id=None):
    if request.method == 'POST':
        setting = request.form.get('setting')
        comment_id = request.form.get('value_0')

        if not setting or not comment_id:
            abort(400)
        try:
            comment_id = int(comment_id)
        except:
            abort(400)

        comment = Comment(comment_id)

        if not comment.id:
            abort(400)

        if setting == 'delete':
            comment.delete()
            flash(messages.comment_deleted)
            return redirect(url_for('admin_comment'))

        else:
            abort(404)

    else:
        if id:
            comment = Comment(id)
            comment = comment.get_comment()

            if not comment:
                flash(messages.comment_not_found)
        else:
            comment = None

        return render_template('admin/comment.html', comment=comment)

