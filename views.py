# -*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, abort, flash
from flaskext.login import login_user, logout_user, current_user

import database
import user
import inputverification
import upload
import exceptions
from post import Posts, NewPost
from comment import Comments, NewComment
from config import POSTSPERSITE, ACCOUNTACTIVATION, TEMPLATES, STYLES

def index():
    pps = postspersite()
    posts = Posts()
    posts = posts.get_post_list()
    page = calcpagelinks( len(posts), 1 )

    return render_template(gettemplate('index.html'), style=getstyle(), posts=posts, \
                           page=page)

def login():
    if request.method == 'POST':
        u = user.User(username=request.form['user'])
        if u.authenticate( request.form['pass'] ):
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

    return render_template(gettemplate('login.html'), style=getstyle())

def logout():
    logout_user()
    flash('Erfolgreich ausgeloggt', 'message')
    return redirect(url_for('index'))

def register():
    if request.method == 'POST':
        if not ('user', 'pass', 'email') in request.form:
            try:
                u = user.NewUser(request.form['user'], request.form['pass'], \
                                 request.form['email'])
            except exceptions.UserAlreadyExists:
                flash(u'Der gewählte Benutzername ist leider schon vorhanden', 'error')
                return redirect(url_for('register'))

            if u.is_active():
                login_user(u)
                flash(u'Erfolgreich registriert: Du bist angemeldet', 'message')
                return redirect(url_for('index'))
            else:
                flash(u'Erfolgreich registriert: Dein Account muss noch vom Administrator \
                        aktiviert werden')
                return redirect(url_for('login'))
        else:
            flash(u'Es wurden nicht alle Felder ausgefüllt', 'error')

    return render_template(gettemplate('register.html'), style=getstyle())

def userpage(name):
    u = user.User(username=name)
    userdict = dict(name=u.username, email=u.email, avatar=u.avatar, active=u.active, \
                    lastlogin=u.lastlogin)
    return render_template(gettemplate('userpage.html'), style=getstyle(), user=userdict)

def usersettings():
    u = current_user
    userdict = dict(name=u.username, email=u.email, avatar=u.avatar, style=u.style, \
                    template=u.template, postspersite=u.postspersite)
    upload.setFileSize('avatars')
    return render_template(gettemplate('usersettings.html'), style=getstyle(), \
                                        user=userdict, templates=TEMPLATES, styles=STYLES)

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
        ul = upload.Upload('avatars')
        ul.save(request.files['avatar'])
        if ul.error: flash(ul.error, 'error'); return redirect(url_for('usersettings'));
        value = ul.url()
    elif field == 'style':
        message = 'Style'
        value = request.form['style']
    elif field == 'template':
        message = 'Template'
        value = request.form['template']
        if value not in TEMPLATES:
            value = 'default'
    elif field == 'delavatar':
        database.updatesetting(userid=u.id, column='avatar', value="")
        flash('Avatar entfernt', 'message')
        return redirect(url_for('usersettings'))
    
    if value:
        database.updatesetting(userid=u.id, column=field, value=value)
        flash("%s erfolgreich editiert" %(message), 'message')
    else:
        flash("Das hat leider nicht geklappt", 'error')
    
    return redirect(url_for('usersettings'))

def newpost(ctype):
    if ctype in ['text', 'audio', 'video', 'link', 'image']:
        return render_template(gettemplate('newpost.html'), style=getstyle(), \
                                posttype=ctype)
    return abort(404)

def addpost():
    newPost = NewPost( request.form )
    try:
        newPost.safe()
        flash("Neuer Eintrag erfolgreich erstellt", 'message')
    except:
        flash("Der Eintrag konnte nicht erstellt werden", 'error')

    return redirect(url_for('index'))

def getpost(id):
    post = Posts(postId=id)
    post = post.get_single_post()
    comments = Comments(postId=id)
    camount = comments.get_comment_amount()
    comments = comments.get_comment_list()

    return render_template(gettemplate('singlepost.html'), style=getstyle(), \
                            post=post, comments=comments, commentamount=camount)

def getposts(filter, pagenumber=1):
    posts = Posts(postFilter=filter, page=pagenumber)
    posts = posts.get_post_list()
    page = calcpagelinks( len(posts), pagenumber )

    return render_template(gettemplate('filteredview.html'), style=getstyle(), \
                            posts=posts, type=filter, page=page)

def getuserposts(username, pagenumber=1):
    posts = Posts(username=username, page=pagenumber)
    posts = posts.get_post_list()
    page = calcpagelinks( len(posts), pagenumber )

    return render_template(gettemplate('filteredview.html'), style=getstyle(), \
                            posts=posts, type='user', page=page, username=username)

def getpage(pagenumber):
    posts = Posts(page=pagenumber)
    posts = posts.get_post_list()

    page = calcpagelinks( len(posts), pagenumber )

    return render_template(gettemplate('page.html'), style=getstyle(), \
                            posts=posts, page=page)

def addcomment():
    try:
        comment = NewComment( request.form )
        comment.safe()
        flash('Kommentar erfolgreich erstellt', 'message')
    except:
        flash('Fehler beim erstellen des Kommentars', 'error')
    return redirect('/posts/'+request.form['relatedpost']+'/')

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

def gettemplate( templatefile ):
    template = None
    try:
        template = current_user.template
    except:
        template = 'default'
    if template:
        return template + '/' + templatefile
    else:
        return 'default/' + templatefile

def getstyle():
    try:
        style = current_user.style
    except:
        style = 'default'
    return style
