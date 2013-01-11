# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, abort
from flask import session, jsonify
from flask.ext.login import login_required
from werkzeug.contrib.atom import AtomFeed

import exceptions
import upload
import config
import messages

from user import User, NewUser, get_current_user, get_posts_per_page
from post import Posts, Post, NewPost
from comment import NewComment
from usersettings import UserSettings


# index
def index():
    if not get_current_user():
        return redirect(url_for('public_index'))

    posts = Posts()
    posts = posts.get_posts()
    page = calc_page_links(len(posts), 1)

    return render_template(get_template('page.html'), posts=posts,
                           page_links=page)


# login, logout, register
def login():
    if request.method == 'POST':
        user = User(name=request.form.get('username'))
        if user.id and user.authenticate(request.form.get('password')):

            if request.form.get('remember_me'):
                user.login(remember=True)
            else:
                user.login(remember=False)

            if user.is_active():
                flash(messages.logged_in, 'message')
            else:
                flash(messages.user_not_activated, 'message')
                return redirect(url_for('public_index'))

            if request.args.get('next'):
                return redirect(request.args['next'])

            return redirect(url_for('index'))
        else:
            flash(messages.invalid_credentials, 'error')

    next = None
    if request.args.get('next'):
        next = request.args['next']
    return render_template(get_template('login.html'), next=next)

def logout():
    if get_current_user():
        get_current_user().logout()
        flash(messages.logged_out, 'message')

    return redirect(url_for('public_index'))

def register():
    if request.method == 'POST' and config.get('registration', bool):
        if 'username' in request.form and 'password' in request.form and \
           'email' in request.form:
            try:
                user = NewUser(request.form['username'],
                               request.form['password'],
                               request.form['email'])
                user.create()
            except exceptions.UserAlreadyExists:
                flash(messages.username_already_exists, 'error')
                return redirect(url_for('register'))
            except:
                flash(messages.register_error, 'error')
                return redirect(url_for('register'))

            if user.is_active():
                user.login()
                flash(messages.registered_and_logged_in, 'message')
                return redirect(url_for('index'))
            else:
                flash(messages.registered_and_deactivated, 'message')
                return redirect(url_for('public_index'))
        else:
            flash(messages.register_field_error, 'error')

    return render_template(get_template('register.html'),
                           registration_enabled=config.get('registration', bool))


# user profile, settings
@login_required
def user_page(name):
    user = User(name=name)
    return render_template(get_template('user_page.html'), user=user)

@login_required
def user_settings():
    if request.method == 'POST':
        setting = UserSettings()
        setting.change()

    user = get_current_user()
    return render_template(get_template('user_settings.html'), user=user,
                           templates=config.get('templates', list))


# post views
@login_required
def get_post(post_id):
    post = Post(post_id=post_id)
    post = post.get_post()

    return render_template(get_template('single_post.html'), post=post)

@login_required
def get_posts(filter, page_number=1):
    posts = Posts(post_filter=filter, page=page_number)
    posts = posts.get_posts()
    page_links = calc_page_links(len(posts), page_number)

    return render_template(get_template('filtered_view.html'), type=filter,
                           posts=posts, page_links=page_links)

@login_required
def get_user_posts(username, page_number=1):
    posts = Posts(username=username, page=page_number)
    posts = posts.get_posts()
    page_links = calc_page_links(len(posts), page_number)

    return render_template(get_template('filtered_view.html'), type='user',
                           posts=posts, page_links=page_links,
                           username=username)

@login_required
def get_page(page_number):
    posts = Posts(page=page_number)
    posts = posts.get_posts()
    page_links = calc_page_links(len(posts), page_number)

    return render_template(get_template('page.html'), posts=posts,
                           page_links=page_links)

@login_required
def get_minimal_post_list():
    posts = Posts(id_list='all')
    posts = posts.get_posts()

    return render_template(get_template('minimal_post_list.html'), posts=posts)


# new post, comment
@login_required
def new_post(post_type):
    if post_type in config.get('post_categories', list):
        if post_type == 'image':
            upload.setFileSize('images')
        elif post_type == 'audio':
            upload.setFileSize('audio')

        return render_template(get_template('new_post.html'), \
                               post_type=post_type)
    abort(404)

@login_required
def add_post():
    try:
        post = NewPost(request.form)
        post.safe()

        flash(messages.post_created, 'message')

    except exceptions.CantCreateNewPost:
        flash(messages.post_error, 'error')
        return redirect(url_for('index'))

    # push this post to facebook?
    if config.get('facebook_integration', bool):
        if get_current_user().facebook_integration and post.is_public:
            return redirect(url_for('facebook_authorize_and_post',
                            post_id=post.id))

    return redirect(url_for('index'))

@login_required
def add_comment():
    try:
        comment = NewComment(request.form)
        comment.safe()

        return redirect('/posts/' + str(comment.related_post) + '/#comments')

    except exceptions.CantCreateNewComment:
        flash(messages.comment_error, 'error')

    return redirect('/posts/' + request.form['related_post'] + '/')


# file upload
@login_required
def handle_upload(file_type):
    if file_type == 'image':
        u = upload.Upload('images')
    elif file_type == 'audio':
        u = upload.Upload('audio')

    try:
        u.save(request.files['file'])

        from base import generate_csrf_token
        return jsonify(url=u.url(), csrf_token=generate_csrf_token(),
                       error='false')
    except:
        return jsonify(error='true')

    abort(404)


# public pages
def public_index():
    posts = Posts(only_public=True)
    posts = posts.get_posts()
    page_links = calc_page_links(len(posts), 1)

    return render_template(get_template('public_page.html'), posts=posts,
                           page_links=page_links)

def public_page(page_number):
    posts = Posts(only_public=True, page=page_number)
    posts = posts.get_posts()
    page_links = calc_page_links(len(posts), page_number)

    return render_template(get_template('public_page.html'), posts=posts,
                           page_links=page_links)

def public_post(public_post_id):
    post = Post(public_id=public_post_id)
    post = post.get_post()

    return render_template(get_template('public_single_post.html'), post=post)

def public_posts(filter, page_number=1):
    posts = Posts(only_public=True, page=page_number, post_filter=filter)
    posts = posts.get_posts()
    page_links = calc_page_links(len(posts), page_number)

    return render_template(get_template('public_filtered_view.html'),
                           posts=posts, page_links=page_links, type=filter)

def public_user_posts(username, page_number=1):
    posts = Posts(only_public=True, page=page_number, username=username)
    posts = posts.get_posts()
    page_links = calc_page_links(len(posts), page_number)

    return render_template(get_template('public_filtered_view.html'),
                           posts=posts, username=username, type='user')


# feeds
@login_required
def feed():
    feed = AtomFeed('Recent posts', feed_url=request.url, url=request.url_root)
    posts = Posts(post_amount=15)
    posts = posts.get_posts()

    for post in posts:
        title = '[' + post.content_type + '] ' + post.title
        feed.add(title, content_type='html', author=post.user.name,
                 updated=post.time, url=url_for('get_post', post_id=post.id,
                 _external=True))

    return feed.get_response()

def public_feed():
    feed = AtomFeed('Recent public posts', feed_url=request.url,
                    url=request.url_root)
    posts = Posts(only_public=True, post_amount=15)
    posts = posts.get_posts()

    for post in posts:
        title = '[' + post.content_type + '] ' + post.title
        feed.add(title, content_type='html', author=post.user.name,
                 updated=post.time, url=url_for('public_post',
                 public_post_id=post.public_id, _external=True))

    return feed.get_response()


# helper functions
def get_template(template_file):
    if hasattr(get_current_user(), 'template'):
        template = get_current_user().template
    else:
        template = config.get('default_template')

    return template + '/' + template_file

def calc_page_links(post_amount, page_number):
    page = dict(number=page_number)
    page['prev'] = page_number-1 if page_number>1 else 0
    page['next'] = page_number+1 if post_amount==get_posts_per_page() else 0
    return page

