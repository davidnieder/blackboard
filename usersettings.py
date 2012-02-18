# -*- coding: UTF-8 -*-

from flask import request

import exceptions
import database
import config
import upload
from user import get_current_user

class UpdateUserSettings():

    def __init__(self, setting, form):
        self.form = form
        self.message = [None, None]
        self.user = get_current_user()

        if self.user == None:
            raise exceptions.NoUserLoggedIn

        if setting == 'password':
            self.change_password()
        elif setting == 'email':
            self.change_email()
        elif setting == 'postspersite':
            self.change_posts_per_site()
        elif setting == 'notification':
            self.change_notification()
        elif setting == 'avatar':
            self.change_avatar()
        elif setting == 'template':
            self.change_template()
        elif setting == 'style':
            self.change_style()
        elif setting == 'delavatar':
            self.def_avatar()
        else:
            raise exceptions.NoSuchSetting


    def change_password(self):
        if self.user.authenticate( self.form['oldpass'] ):
            if self.form['newpass1'] == self.form['newpass2']:

                database.updatesetting(userid=self.user.id, column='password',\
                                       value=self.form['newpass1'])

                self.message[0] = u'Passwort erfolgreich geändert'
                self.message[1] = 'message'
            else:
                self.message[0] = u'Die Passwörter stimmen nicht überein'
                self.message[1] = 'error'
        else:
            self.message[0] = u'Das alte Passwort stimmt nicht'
            self.message[1] = 'error'

    def change_email(self):
        # implement: validate email address
        database.updatesetting(userid=self.user.id, column='email', \
                               value=self.form['newemail'])
        self.message[0] = u'E-Mail-Adresse erfolgreich geändert'
        self.message[1] = 'message'

    def change_notification(self):
        if self.form['emailnotification'] in ['0', '1']:
            database.updatesetting(userid=self.user.id, \
                                   column='emailnotification', \
                                   value=self.form['emailnotification'])

            if int(self.form['emailnotification']) == 1:
                self.message[0] = u'E-Mail Benachrichtigung eingeschaltet'
                self.message[1] = 'message'
            else:
                self.message[0] = 'E-Mail Benachrichtigung ausgeschaltet'
                self.message[1] = 'message'
        else:
            self.message[0] = u'Das hat leider nicht geklappt'
            self.message[1] = 'error'

    def change_posts_per_site(self):
        if self.form['postspersite'] in ['5','10','15']:
            database.updatesetting(userid=self.user.id, \
                                   column='postspersite', \
                                   value=self.form['postspersite'])

            self.message[0] = u'Einträge pro Seite erfolgreich geändert'
            self.message[1] = u'message'
        else:
            self.message[0] = u'Das hat leider nicht geklappt'
            self.message[1] = 'error'


    def change_avatar(self):
        ul = upload.Upload('avatar')
        ul.save(request.files['avatar'])

        if ul.error:
            self.message[0] = u'Avatar konnte nicht hochgeladen werden'
            self.message[1] = 'errir'
        else:
            database.updatesetting(userid=self.user.id, column='avatar', \
                                   value=ul.url())

            self.message[0] = 'Avatar erfolgreich aktualisiert'
            self.message[1] = 'message'

    def del_avatar(self):
        database.updatesetting(userid=self.user.id, column='avatar', \
                               value='')

        self.message[0] = u'Avatar erfolgreich gelöscht'
        self.message[1] = 'message'

    def change_template(self):
        if self.form['template'] in config.TEMPLATES:
            database.updatesetting(userid=self.user.id, column='template', \
                                   value=self.form['template'])

            self.message[0] = u'Template erfolgreich geändert'
            self.message[1] = 'message'
        else:
            self.message[0] = u'Template konnte nicht geändert werden'
            self.message[1] = 'error'


    def change_style(self):
        if self.form['style'] in config.STYLES:
            database.updatesetting(userid=self.user.id, column='style', \
                                   value=self.form['style'])

            self.message[0] = u'Style erfolgreich geändert'
            self.message[1] = 'message'
        else:
            self.message[0] = u'Style konnte nicht geändert werden'
            self.message[1] = 'error'

    def get_message_as_dict(self):
        return dict(messageText=message[0], messageType=message[1])

    def get_message_as_list(self):
        return self.message

