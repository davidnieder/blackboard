# -*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, abort, flash
from flaskext.login import login_user, logout_user, current_user

import database
import user
import inputverification
from config import POSTSPERSITE, ACCOUNTACTIVATION

def index():
    pps = postspersite()
    posts = database.getentries(i=pps, topost=pps)
    page = calcpagelinks( len(posts), 1 )

    return render_template('index.html', posts=posts, page=page)

def login():
    if request.method == 'POST':
        u = user.User(username=request.form['username'])
        if u.authenticate( request.form['password'] ):
            login_user(u, remember=True)
            database.updatelogindate(u.id)
            if u.is_active():
                flash('Du hast dich erfolgreich angemeldet', 'message')
            else:
                flash('Dein Account wartet noch auf Aktivierung', 'message')
            #if request.form['next']:
            #    return redirect(url_for(request.form['next']))
            return redirect(url_for('index'))
        else:
            flash('Falscher Benutzername oder falsches Passwort', 'error')

    return render_template('login.html')

def logout():
    logout_user()
    flash('Erfolgreich ausgeloggt', 'message')
    return redirect(url_for('index'))

def register():
    if request.method == 'POST':
        u = user.User(username=request.form['user'])
        if not u.username:
            if user.new(request.form['user'], request.form['pass'], request.form['email']):
                flash('Erfolgreich registriert', 'message')
                if not ACCOUNTACTIVATION:
                    u = user.User(username=request.form['user'])
                    if u.authenticate( request.form['password']):
                        login_user(u)
                return redirect(url_for('index'))
            else:
                flash('Fehler bei der Registrierung', 'error')
        else:
            flash(u'Der gewählte Benutzername ist leider schon vorhanden', 'error')
    return render_template('register.html')

def userpage(name):
    u = user.User(username=name)
    userdict = dict(name=u.username, email=u.email, avatar=u.avatar, active=u.active, \
                    lastlogin=u.lastlogin)
    return render_template('userpage.html', user=userdict)

def usersettings():
    u = current_user
    userdict = dict(name=u.username, email=u.email, avatar=u.avatar, style=u.style, \
                    template=u.template, postspersite=u.postspersite)
    return render_template('usersettings.html', user=userdict)

def changesettings(field):
    # VERIFICATION!!!
    u = current_user
    value = None
    message = None

    if field == 'password':
        message = "Passwort"
        if u.authenticate( request.form['oldpass'] ):
            value = request.form['newpass1']

    elif field == 'email':
        message = 'E-Mail-Adresse'
        value = request.form['newemail']
    elif field == 'postspersite':
        message = 'Beitragszahl pro Seite'
        value = int( request.form['postspersite'] )
    elif field == 'notification':
        message = 'E-Mail-Benachrichtigung'
        value = int( request.form['emailnotification'] )
    elif field == 'avatar':
        message = 'Avatar'
        pass
    elif field == 'style':
        message = 'Style'
        value = request.form['style']
    elif field == 'template':
        message = 'Template'
        value = request.form['template']
    
    if value:
        database.updatesetting(userid=u.id, column=field, value=value)
        flash("%s erfolgreich editiert" %(message), 'message')
    else:
        flash("Das hat leider nicht geklappt", 'error')
    
    return redirect(url_for('usersettings'))

def newpost(ctype):
    if ctype in ['text', 'audio', 'video', 'link', 'image']:
        return render_template('newpost.html', posttype=ctype)
    return abort(404)

def addpost():
    form = inputverification.NewPostForm( request.form )
    if form.verify:
        database.addentry( request.form, current_user.username )
        flash('Neuer Post erfolgreich erstellt', 'message')
    else:
        flash('Fehler', 'error')

    return redirect(url_for('index'))

def getpost(id):
    post = database.getpost(id)
    return render_template('singlepost.html', post=post)

def getposts(filter, pagenumber=1):
    posts_per_site = postspersite()
    posts = database.getposts(filter, (pagenumber-1)*posts_per_site, \
                                pagenumber*posts_per_site)
    page = calcpagelinks( len(posts), pagenumber )

    return render_template('filteredview.html', posts=posts, type=filter, page=page)

def getuserposts(username, pagenumber=1):
    posts_per_site = postspersite()
    posts = database.getuserposts(username, (pagenumber-1)*posts_per_site, \
                                pagenumber*posts_per_site)
    page = calcpagelinks( len(posts), pagenumber )

    return render_template('filteredview.html', posts=posts, type='user', page=page, \
                            username=username)

def getpage(pagenumber):
    pps = postspersite()

    posts = database.getentries(pagenumber*pps, \
                                (pagenumber-1)*pps, \
                                pagenumber*pps )
    #posts = database.getentries(i=pps, topost=pps)
    page = calcpagelinks( len(posts), pagenumber )

    return render_template('page.html', posts=posts, page=page)

# helper functions
def calcpagelinks( postamount, pagenumber ):
    page = dict(number=pagenumber)
    page['prev'] = pagenumber-1 if pagenumber>1 else 0
    page['next'] = pagenumber+1 if postamount==postspersite() else 0

    return page

def postspersite():
    try:
        return current_user.postspersite
    except:
        return POSTSPERSITE