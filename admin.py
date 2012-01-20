# -*- coding: UTF-8 -*-

from flask import render_template, url_for, flash, redirect, request
from flaskext.login import current_user

import database
from user import User
from post import Posts, PublicPost, new_public_link
from config import NOADMINACCESS

def index():
    if not userisadmin():
        flash(NOADMINACCESS, 'error')
        return redirect(url_for('index'))

    return render_template('admin/index.html')

def user():
    if not userisadmin():
        flash(NOADMINACCESS, 'error')
        return redirect(url_for('index'))

    users = database.getusers()
    return render_template('admin/user.html', userlist=users)

def userdetail(id):
    if not userisadmin():
        flash(NOADMINACCESS, 'error')
        return redirect(url_for('index'))

    user = database.getuser(id)
    return render_template('admin/user_detail.html', user=user)

def deluser(id):
    if not userisadmin():
        flash(NOADMINACCESS, 'error')
        return redirect(url_for('index'))

    database.deluser(id)
    return redirect(url_for('admin_user'))

def activate(id):
    if not userisadmin():
        flash(NOADMINACCESS)
        return redirect(url_for('index'))

    user = User(id=id)
    active = 0 if user.active else 1
    database.activateuser(id, active)
    return redirect(url_for('admin_user'))

def setpw(id):
    if not userisadmin():
        flash(NOADMINACCESS, 'error')
        return redirect(url_for('index'))

    if request.form['pw']:
        database.updatesetting(id, 'password', request.form['pw'])
        flash('Password gesetzt')

    return redirect(url_for('admin_user'))

def post(id):
    if not userisadmin():
        flash(NOADMINACCESS, 'error')
        return redirect(url_for('index'))
    post = {}
    public = False
    if id:
        post = Posts(postId=id)
        post = post.get_single_post()
    if id and not post:
        flash("Eintrag #%s nicht gefunden" %id)
    else:
        try:
            public = PublicPost(post_id=post['id'])
            public = public.get_public_id()
        except:
            public = False

    return render_template('admin/del_post.html', post=post, public=public)

def delpost(id):
    if not userisadmin():
        flash(NOADMINACCESS, 'error')
        return redirect(url_for('index'))

    post = Posts(postId=id)

    if post.delete():
        flash(u'Post gelöscht')
    else:
        flash(u'Post konnte nicht gelöscht werden')
    return redirect(url_for('admin_posts'))

def setpublic(postId):
    if not userisadmin():
        flash(NOADMINACCESS, 'error')
        return redirect(url_for('index'))

    #to implement: check if post exists
    new_public_link(postId)
    return redirect(url_for('admin_post_show', id=postId))

# helper
def userisadmin():
    try:
        return current_user.admin
    except:
        return False


