# -*- coding: utf-8 -*-

from flask import request, flash, abort

import config
import messages
from user import get_current_user


class UserSettings():

    def __init__(self):

        self.setting = request.form.get('setting')
        self.value = request.form.get('value')
        self.old_value = request.form.get('old_value')
        self.user = get_current_user()

        if not self.setting or not self.value:
            abort(400)

        if self.setting == 'password':
            self.change = self.change_password
        elif self.setting == 'email':
            self.change = self.change_email
        elif self.setting == 'posts_per_page':
            self.change = self.change_posts_per_page
        elif self.setting == 'email_notification':
            self.change = self.change_email_notification
        elif self.setting == 'template':
            self.change = self.change_template
        elif self.setting == 'facebook_integration':
            self.change = self.change_facebook_integration
        else:
            abort(400)

    def change_password(self):
        if self.old_value:
            if self.user.authenticate(self.old_value):
                self.user.set_password(self.value)
                flash(messages.changed_password, 'message')
            else:
                flash(messages.wrong_password, 'error')
        else:
            abort(400)

    def change_email(self):
        self.user.update_setting('email', self.value)
        flash(messages.changed_email, 'message')

    def change_posts_per_page(self):
        if self.value in config.get('posts_per_page_options', list):
            self.user.update_setting('posts_per_page', int(self.value))
            flash(messages.changed_setting, 'message')
        else:
            abort(400)

    def change_email_notification(self):
        if self.value in ['True', 'False']:
            if self.value == 'True':
                self.user.update_setting('email_notification', True)
            else:
                self.user.update_setting('email_notification', False)
            flash(messages.changed_setting, 'message')
        else:
            abort(400)

    def change_template(self):
        if self.value in config.get('templates', list):
            self.user.update_setting('template', self.value)
            flash(messages.changed_template, 'message')
        else:
            abort(400)

    def change_facebook_integration(self):
        if self.value in ['True', 'False']:
            if self.value == 'True':
                self.user.update_setting('facebook_integration', True)
            else:
                self.user.update_setting('facebook_integration', False)
            flash(messages.changed_facebook_integration, 'message')
        else:
            abort(400)

