# -*- coding: UTF-8 -*-

import database
import inputverification
import time
import hashlib
import exceptions
import comment
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
            if self.postFilter:
                # add a filter
                pass
            else:
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
        self.addCommentAmount()
        self.prepare_posts()

    def addAvatar(self):
        usernames = []
        for hashmap in self.postList:
            usernames.append( hashmap[self.postTableColumns['user']] )
        usernames = set(usernames)

        avatarDict = {}
        for user in usernames:
            avatarDict[user] = get_avatar(user)

        for post in self.postList:
            if avatarDict.has_key( post[self.postTableColumns['user']] ):
                post.update( avatar=avatarDict[post[self.postTableColumns['user']]] )

    def addCommentAmount(self):
        for post in self.postList:
            commentAmount = comment.Comments( post[self.postTableColumns['id']] )
            commentAmount = commentAmount.get_comment_amount()
            post.update( comments=commentAmount )

    def get_posts_per_site(self):
        try:
            self.postsPerSite = get_current_user().postspersite
        except:
            self.postsPerSite = POSTSPERSITE

    def get_post_list(self):
        return self.postList

    def get_single_post(self):
        if self.postList:
            return self.postList[0]
        else:
            return None

    def prepare_posts(self):
        for post in self.postList:
                post[self.postTableColumns['contenttype']] = \
                contentkey[post[self.postTableColumns['contenttype']]]

                post.update(date = post[self.postTableColumns['date']])
                post.pop(self.postTableColumns['date'])

                try:
                    public_id = PublicPost( post_id=post[self.postTableColumns['id']] )
                    public_id = public_id.get_public_id()
                    if public_id:
                        post.update(public_link = public_id)
                except exceptions.NoPublicPostId:
                    pass

    def delete(self):
        if self.postId:
            database.delpost(self.postId)
            return True
        return False

class NewPost():

    def __init__(self, form):
        self.form = form
        inputverification.NewPostForm( form )

    def safe(self):
        self.get_keys()

        try:
            if self.contenttype == 'text':
                self.post_id = database.commit( 'posts', ['title', 'text', \
                                                'contenttype', 'time', 'user'], \
                                [self.title, self.text, contentkey['text'], self.date, \
                                 self.user] )

            elif self.contenttype in ['link', 'image']:
                self.post_id = database.commit( 'posts', ['title', 'text', \
                                                'contenttype', 'url', 'time', 'user'], \
                                [self.title, self.text, contentkey[self.contenttype], \
                                 self.url, self.date, self.user] )

            elif self.contenttype in ['audio', 'video']:
                self.post_id = database.commit( 'posts', ['title', 'text', \
                                                'contenttype', 'code', 'time', 'user'], \
                                [self.title, self.text, contentkey[self.contenttype], \
                                 self.code, self.date, self.user] )
        except:
            raise exceptions.CantCreateNewPost

        if self.is_public:
            new_public_link( self.post_id[0] )


    def get_keys(self):
        try:
            self.contenttype = self.form['contenttype']
            self.title = self.form['title']

            if self.contenttype == 'text':
                self.text = self.form['content']
            else:
                self.text = self.form['comment']

            if self.contenttype in ['link', 'image']:
                self.url = self.form['link']

            elif self.contenttype in ['audio', 'video']:
                self.code = self.form['code']

            self.date = time.strftime('%d.%m.%y')
            self.user = get_current_user().username
            if not self.user:
                raise exceptions.NoUserLoggedIn

        except:
            raise exceptions.CantCreateNewPost

        try:
            if self.form['public_post']  == '1':
                self.is_public = True
            else:
                self.is_public = False
        except:
            self.is_public = False


class PublicPost():

    def __init__(self, public_id=None, post_id=None):
        self.public_id = public_id
        self.post_id = post_id

    def get_post_id(self):
        if self.public_id:
            r = database.query('SELECT post_id FROM public_posts WHERE \
                                public_id=\'%s\' LIMIT 1' %(self.public_id) )
            try:
                return r[0]['post_id']
            except:
                raise exception.NoSuchPostId
        else:
            raise exceptions.NoSuchPostId

    def get_public_id(self):
        if self.post_id:
            r = database.query( 'SELECT public_id FROM public_posts WHERE \
                                 post_id=\'%s\' LIMIT 1' %(self.post_id) )
            try:
                return r[0]['public_id']
            except:
                raise exceptions.NoPublicPostId
        else:
            raise exceptions.NoPublicPostId

def new_public_link( post_id ):
    # to implement: check for double hashes
    md5_hash = hashlib.md5()
    md5_hash.update( str(post_id) + str(time.time()) )
    public_id = md5_hash.hexdigest()[:5]
    database.commit( 'public_posts', ['public_id', 'post_id'], [public_id, post_id] )

