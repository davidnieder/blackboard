# -*- coding: utf-8 -*-

from datetime import datetime
from time import time

from flask import redirect, request, url_for, flash
from flask.ext.login import login_required
from flaskext.oauth import OAuth

import config
from database import db, Facebook as DBFacebook
from user import get_current_user
from post import Post


oauth = OAuth()

facebook = oauth.remote_app(
                name='facebook',
                base_url='https://graph.facebook.com/',
                request_token_url=None,
                access_token_url='/oauth/access_token',
                authorize_url='https://www.facebook.com/dialog/oauth',
                consumer_key=config.get('facebook_app_id'),
                consumer_secret=config.get('facebook_app_secret'),
                request_token_params={'scope': 'publish_stream'}
            )


@login_required
def authorization():
    return facebook.authorize(callback=url_for('facebook_authorized',
                              next=request.args.get('next') or url_for('index'),
                              _external=True))

@facebook.authorized_handler
@login_required
def authorized(response):
    if response is None:
        #flash(u'Facebook-Access denied: reason=%s, error=%s' \
        #      %(request.args['error_reason'],
        #        request.args['error_description']),
        #      'error')
        flash(messages.fb_access_denied, 'error')

    else:
        oauth_token = response['access_token']
        expires = int(response['expires']) + time()

        if get_current_user():
            user_id = get_current_user().id
            db_obj = DBFacebook.query.filter_by(user_id=user_id).first()
            if db_obj:
                db_obj.access_token = oauth_token
                db_obj.expire_time = datetime.utcfromtimestamp(expires)
            else:
                db_obj = DBFacebook(
                            user_id=get_current_user().id,
                            access_token=oauth_token,
                            expire_time=datetime.utcfromtimestamp(expires)
                        )

            db.session.add(db_obj)
            db.session.commit()

    return redirect(request.args.get('next') or url_for('index'))

@facebook.tokengetter
def get_facebook_oauth_token():

    user = get_current_user()
    if not user:
        return None

    db_obj = DBFacebook.query.filter_by(user_id=user.id).first()

    if not db_obj:
        return None

    if not db_obj.access_token:
        return None

    if db_obj.expire_time < datetime.utcnow():
        return None

    return db_obj.access_token, ''

@login_required
def authorize_and_post(post_id):
    return redirect(url_for('facebook_authorization',
                            next=url_for('facebook_push_post',
                                         post_id=post_id)))

@login_required
def push_post(post_id):
    # check if post exists
    post = Post(post_id=post_id)
    if not post.id:
        flash(messages.fb_invalid_post_id, 'error')
        return redirect(url_for('index'))

    # check if post is public
    if not post.is_public:
        flash(messages.fb_post_is_private, 'error')
        return redirect(url_for('index'))

    # create wall post message
    if post.content_type in ['video', 'image', 'link', 'text']:
        message = 'I just posted a new ' + post.content_type + ' on blackboard.'
    elif post.content_type == 'audio':
        message = 'I just posted a new song on blackboard'
    else:
        flash(messages.fb_invalid_post_type, 'error')
        return redirect(url_for('index'))

    # create wall post link name
    if post.title:
        title = post.title
    else:
        title = 'View this post'

    # create url for this post
    url = url_for('public_post', public_post_id=post.public_id, _external=True)

    data = dict(message=message, link=url, name=title)
    response = facebook.post(url='/me/feed', data=data, format='urlencoded')

    if response.data.get('error'):
        #flash(u'Facebook-Push: %s' %response.data['error'], 'error')
        flash(messages.fb_error_returned, 'error')

    return redirect(url_for('index'))

