# -*- coding: UTF-8 -*-

import database
from config import POSTSPERSITE
from user import get_avatar, get_current_user, get as get_username

contentkey = {  'text':  1, 1: 'text',
                'image': 2, 2: 'image',
                'video': 3, 3: 'video',
                'link':  4, 4: 'link',
                'audio': 5, 5: 'audio'  }

class Posts():

    def __init__(self, postId=None, username=None, userid=None, page=1, \
                       postFilter=None):

        self.postId = postId
        self.username = username
        self.userid = userid
        self.postFilter = postFilter
        self.page = page

        self.get_posts_per_site()

        self.postTable = 'posts'
        self.postTableColumns = {'id':'id', 'title':'title', 'text':'text', \
                                 'url':'url', 'code':'code', 'date':'time', \
                                 'contenttype': 'contenttype', 'user':'user'}
        self.userTable = 'users'
        self.userTableColumns = 'avatar'

        if self.username or self.userid:
            # Get user posts
            if self.userid:
                self.username = get_username(self.userid)

            self.get_posts( str(self.postTableColumns['user']) + \
                            '=\'%s\'' %self.username )
        elif self.postFilter:
            # Filtered view e.g. /posts/audio/
            self.get_posts( str(self.postTableColumns['contenttype']) + \
                            '=%s' %contentkey[self.postFilter] )
        elif self.postId:
            # Get special post
            self.get_posts( str(self.postTableColumns['id']) + \
                            '=%i' %self.postId )
        else:
            # Get index page
            self.get_posts('1')


    def get_posts(self, condition):
        columns = ''
        for column in self.postTableColumns.values():
            columns += column + ', '
        columns = columns[:-2]

        query  = 'SELECT ' + columns + ' '
        query += 'FROM ' + self.postTable + ' '
        query += 'WHERE ' + condition + ' ORDER BY id DESC '
        query += 'LIMIT ' + str( self.postsPerSite ) + ' '
        query += 'OFFSET ' + str( (self.page-1)*self.postsPerSite ) + ''

        self.postList = database.query( query )
        self.addAvatar()
        self.prepare_posts()

    def addAvatar(self):
        usernames = []
        for hashmap in self.postList:
            usernames.append( hashmap[self.postTableColumns['user']] )
        usernames = set(usernames)

        avatarDict = {}
        for user in usernames:
            avatarDict.update(user=get_avatar(user))

        for post in self.postList:
            if avatarDict.has_key( post[self.postTableColumns['user']] ):
                post.update( avatar=avatarDict[post[self.postTableColumns['user']]] )

    def get_posts_per_site(self):
        if get_current_user():
            self.postsPerSite = get_current_user().postspersite
        else:
            self.postsPerSite = POSTSPERSITE

    def get_post_list(self):
        return self.postList

    def prepare_posts(self):
        for post in self.postList:
                post[self.postTableColumns['contenttype']] = \
                contentkey[post[self.postTableColumns['contenttype']]]

                post.update(date = post[self.postTableColumns['date']])
                post.pop(self.postTableColumns['date'])

    def delete(self):
        if self.postId:
            database.delpost(self.postId)
            return True
        return False


class NewPost():

    def __init__(self):
        pass

    def safe(self):
        pass
