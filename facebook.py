# -*- coding: UTF-8 -*-

import urllib, urlparse
import time
import json

from flask import request, redirect
from user import get_current_user
import database
import exceptions

facebook_app_id = ''
facebook_app_secret = ''

redirect_url = ''
permission_scope = 'publish_stream'


class Facebook():

    def __init__(self):
        user = get_current_user()
        if user:
            self.userid = user.id
        else:
            raise exceptions.NoUserLoggedIn

        self.is_active = self.fb_integration_is_active()
        self.is_authenticated = self.app_is_authenticated()

        self.action_after_response = None
        self.after_response_args = None

    def fb_integration_is_active(self):
        q = database.query('SELECT active FROM facebook WHERE user_id=%i' \
                            %self.userid)
        if q:
            return True if q[0]['active'] else False

    def activate_fb_integration(self):
        if database.check_if_entry_exists('facebook', 'user_id', self.userid):
            database.update_facebook_setting(self.userid, 'active', 1)
        else:
            database.commit('facebook', ['user_id', 'active'], \
                            [self.userid, 1])
            
    def deactivate_fb_integration(self):
        database.update_facebook_setting(self.userid, 'active', 0)

    def app_is_authenticated(self):
        q = database.query('SELECT expire_time, access_token  FROM facebook \
                            WHERE user_id=%i' %self.userid)
        if q:
            expire_time = q[0]['expire_time']
            access_token = q[0]['access_token']

            if not expire_time or not access_token:
                return False
        else:
            return False

        if time.time() < (expire_time-30) and access_token:
            return True
        return False

    def get_auth_token(self):
        q = database.query('SELECT access_token FROM facebook WHERE \
                            user_id=%i' %self.userid)
        if q and q[0].has_key('access_token'):
            return q[0]['access_token']
        return False

    def remember_access_token(self):
        database.update_facebook_setting(self.userid, 'access_token', \
                                         self.access_token)
        database.update_facebook_setting(self.userid, 'expire_time', \
                                         self.expire_time+time.time()-2 )


    def authenticate_app(self):
        return self.request_auth_token() 

    def request_auth_token(self):
        args = dict(client_id=facebook_app_id, scope=permission_scope, \
                    redirect_uri=redirect_url)

        if self.action_after_reponse == 'post' and self.after_response_args:
            args['redirect_uri'] += 'post/'
            args['redirect_uri'] += str(self.after_response_args) + '/'

        return redirect('https://www.facebook.com/dialog/oauth?' + \
                        urllib.urlencode(args))

    def handle_fb_auth_response(self):
        if 'code' in request.args:
            returned_code = request.args['code']

            args = dict(client_id=facebook_app_id, \
                        client_secret=facebook_app_secret, \
                        redirect_uri=redirect_url, code=returned_code)

            response = urllib.urlopen('https://graph.facebook.com/oauth/' + \
                                      'access_token?' + urllib.urlencode(args))
            response = response.read()

            if response[:12] == 'access_token':
                response = urlparse.parse_qs(response)
                self.access_token = response['access_token'][0]
                self.expire_time = response['expires'][0]
                self.expire_time = float(self.expire_time)
            else:
                raise exceptions.AuthenticationFailed

            self.remember_access_token()

        else:
            raise exceptions.AuthenticationFailed

    def push_post_to_wall(self, post_url, post_type, post_title=None):
        if not self.is_authenticated:
           raise exceptions.AppIsNotAuthenticated

        access_token = self.get_auth_token()
        if not access_token:
           raise exceptions.AppIsNotAuthenticated

        # post message 
        if post_type in ['video', 'image', 'link', 'text']:
            message = 'I just posted a new ' + post_type + ' on blackboard.'
        elif post_type == 'audio':
            message = 'I just posted a new song on blackboard.'
        else:
            raise exceptions.CantPostToWall

        # link name
        if post_title:
            title = post_title
        else:
            title = 'Watch/Listen/Read it.'

        args = dict(message=message, link=post_url, name=title, \
                    access_token=access_token)

        response = urllib.urlopen('https://graph.facebook.com/me/feed', \
                                 data=urllib.urlencode(args))
        response = response.read()
        response = json.loads(response)

        if response.has_key('id'):
            # id of the just created wall post
            pass
        if response.has_key('error'):
            # an error occurred
            raise exceptions.CantPostToWall

