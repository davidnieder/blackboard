# -*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, abort, flash
from flaskext.login import login_user, logout_user, current_user

import database
import user
import upload
import exceptions
from post import Posts, NewPost, PublicPost
from comment import Comments, NewComment
from config import POSTSPERSITE, ACCOUNTACTIVATION, TEMPLATES, STYLES
from usersettings import UpdateUserSettings
from facebook import Facebook

def index():
    pps = posts_per_site()
    posts = Posts()
    posts = posts.get_post_list()
    page = calc_page_links( len(posts), 1 )

    return render_template(get_template('index.html'), style=get_style(), \
                           posts=posts, page=page)

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
                return redirect(url_for('login'))

            return redirect(url_for('index'))

        else:
            flash('Falscher Benutzername oder falsches Passwort', 'error')

    return render_template(get_template('login.html'), style=get_style())

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
                flash(u'Der gewählte Benutzername ist leider schon vorhanden', \
                      'error')
                return redirect(url_for('register'))

            if u.is_active():
                login_user(u)
                flash(u'Erfolgreich registriert: Du bist angemeldet', 'message')
                return redirect(url_for('index'))
            else:
                flash(u'Erfolgreich registriert: Dein Account muss noch vom \
                       Administrator aktiviert werden')
                return redirect(url_for('login'))
        else:
            flash(u'Es wurden nicht alle Felder ausgefüllt', 'error')

    return render_template(get_template('register.html'), style=get_style())

def userpage(name):
    u = user.User(username=name)
    userdict = dict(name=u.username, email=u.email, avatar=u.avatar, \
                    active=u.active, lastlogin=u.lastlogin)
    return render_template(get_template('userpage.html'), style=get_style(), \
                           user=userdict)

def usersettings():
    u = current_user
    userdict = dict(name=u.username, email=u.email, avatar=u.avatar, \
                    style=u.style, postspersite=u.postspersite, \
                    facebookintegration=u.facebookintegration, \
                    template=u.template)

    upload.setFileSize('avatars')
    return render_template(get_template('usersettings.html'), user=userdict, \
                           style=get_style(), templates=TEMPLATES, styles=STYLES)

def changesetting(setting):
    updateSetting = UpdateUserSettings( setting, request.form )
    message = updateSetting.get_message_as_list()

    flash(message[0], message[1])

    return redirect(url_for('usersettings'))

def newpost(ctype):
    if ctype in ['text', 'audio', 'video', 'link', 'image']:
        if ctype == 'image':
            upload.setFileSize('images')
        elif ctype == 'audio':
            upload.setFileSize('audio')

        return render_template(get_template('newpost.html'), posttype=ctype, \
                               style=get_style())
    return abort(404)

def addpost():
    try:
        newPost = NewPost( request.form )
        newPost.safe()

        flash("Neuer Eintrag erfolgreich erstellt", 'message')

        # push this post to facebook?
        if current_user.facebookintegration and newPost.is_public:
            return redirect(url_for('facebook_push_post', \
                                    post_id=newPost.get_id()))

    except exceptions.CantCreateNewPost:
        flash("Der Eintrag konnte nicht erstellt werden", 'error')

    return redirect(url_for('index'))

def getpost(id):
    post = Posts(postId=id)
    post = post.get_single_post()
    comments = Comments(postId=id)
    camount = comments.get_comment_amount()
    comments = comments.get_comment_list()

    return render_template(get_template('singlepost.html'), style=get_style(), \
                           post=post, comments=comments, commentamount=camount)

def getposts(filter, pagenumber=1):
    posts = Posts(postFilter=filter, page=pagenumber)
    posts = posts.get_post_list()
    page = calc_page_links( len(posts), pagenumber )

    return render_template(get_template('filteredview.html'), style=get_style(), \
                           posts=posts, type=filter, page=page)

def getuserposts(username, pagenumber=1):
    posts = Posts(username=username, page=pagenumber)
    posts = posts.get_post_list()
    page = calc_page_links( len(posts), pagenumber )

    return render_template(get_template('filteredview.html'), style=get_style(), \
                           posts=posts, type='user', page=page, username=username)

def getpage(pagenumber):
    posts = Posts(page=pagenumber)
    posts = posts.get_post_list()

    page = calc_page_links( len(posts), pagenumber )

    return render_template(get_template('page.html'), style=get_style(), \
                            posts=posts, page=page)

def getminimalpostlist():
    posts = Posts(postId='all')
    posts = posts.get_post_list()

    return render_template(get_template('minimal_post_list.html'), \
                           style=get_style(), posts=posts)

def addcomment():
    try:
        comment = NewComment( request.form )
        comment.safe()
        flash('Kommentar erfolgreich erstellt', 'message')

    except:
        flash('Fehler beim erstellen des Kommentars', 'error')

    else:
        return redirect('/posts/' + str(comment.relatedPost) + '/#comments')

    return redirect('/posts/'+request.form['relatedpost']+'/')

def handle_upload(utype):
    if utype == 'image':
        u = upload.Upload('images')
    elif utype == 'audio':
        u = upload.Upload('audio')

    try:
        u.save(request.files['file'])
        return u.url()
    except:
        return "error"

    abort(404)

def public_link( public_post_id ):
    try:
        post_id = PublicPost( public_id=public_post_id )
        post_id = post_id.get_post_id()

        post = Posts(postId=post_id)
        post = post.get_single_post()

    except:
        abort(404)

    return render_template( get_template('public_view.html'), style=get_style(), \
                            post=post )

# facebook auth
def facebook_authentication():
    fb = Facebook()
    return fb.authenticate_app()

def facebook_handle_response(action=None, arg=None):
    fb = Facebook()
    fb.handle_fb_auth_response()

    if action:
        if action == 'post' and arg:
            return redirect(url_for('facebook_push_post', post_id=arg))
    else:
        return redirect(url_for('index'))

def facebook_push_post(post_id):
    fb = Facebook()
    if fb.app_is_authenticated():
        post = Posts(postId=post_id).get_single_post()
        if not post:
            flash(u'Konnte nicht auf Facebook posten: Post-Id ungültig', \
                  'error')
            return redirect(url_for('index'))

        publicPost = PublicPost(post_id=post_id)
        try:
            public_id = publicPost.get_public_id()
            post_title = post['title']

            post_url = request.url_root + 'public/' + str(public_id) + '/'
            fb.push_post_to_wall(post_url=post_url, post_title=post_title, \
                                      post_type=post['contenttype'])

        except exceptions.NoPublicPostId:
            flash(u'Konnte nicht auf Facebook posten: Post ist nicht \
                    öffentlich', 'error')
        except exceptions.AppIsNotAuthenticated:
            flash(u'Konnte nicht auf Facebook posten: Authentifizierung \
                    gescheitert', 'error')
        except exceptions.CantPostToWall:
            flash(u'Konnte nicht auf Facebook posten', 'error')

        return redirect(url_for('index'))

    else:
        fb.action_after_response = 'post'
        fb.after_response_args = dict(post_id=post_id)
        return fb.authenticate_app()

# helper functions
def calc_page_links( postamount, pagenumber ):
    page = dict(number=pagenumber)
    page['prev'] = pagenumber-1 if pagenumber>1 else 0
    page['next'] = pagenumber+1 if postamount==posts_per_site() else 0

    return page

def posts_per_site():
    try:
        return current_user.postspersite
    except:
        return POSTSPERSITE

def get_template( templatefile ):
    template = None
    try:
        template = current_user.template
    except:
        template = 'default'
    if template:
        return template + '/' + templatefile
    else:
        return 'default/' + templatefile

def get_style():
    try:
        style = current_user.style
    except:
        style = 'default'
    return style
