# -*- coding: UTF-8 -*-

from flask import render_template, url_for, flash, redirect, request
from flaskext.login import current_user

import database
from user import User
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
    post = []
    if id:
        post = database.getpost(id)
    if id and not post:
        flash("Eintrag #%s nicht gefunden" %id)
    return render_template('admin/del_post.html', post=post)

def delpost(id):
    if not userisadmin():
        flash(NOADMINACCESS, 'error')
        return redirect(url_for('index'))

    if database.delpost(id):
        flash(u'Post gelöscht')
    else:
        flash(u'Post konnte nicht gelöscht werden')
    return redirect(url_for('admin_posts'))

# helper
def userisadmin():
    try:
        return current_user.admin
    except:
        return False


