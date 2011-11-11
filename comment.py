# -*- coding: UTF-8 -*-

import database
import exceptions
import time
import inputverification
from user import get_current_user

commentTable = 'comments'
commentTableColumns = { 'comment': 'comment',
                        'relatedPost': 'relatedpost',
                        'user': 'userid',
                        'date': 'time' }

class Comments():

    def __init__(self, postId):
        self.relatedPost = postId
        self.comments = []

    def get_comments(self):
        self.comments = database.query( 'SELECT ' +  \
                                            commentTableColumns['user'] + ', ' + \
                                            commentTableColumns['comment'] + ', ' + \
                                            commentTableColumns['date'] + ' ' +\
                                        'FROM ' + commentTable + ' ' + \
                                        'WHERE ' +  commentTableColumns['relatedPost'] + \
                                        ' =%i' %self.relatedPost )
    def get_comment_list(self):
        self.get_comments()
        return self.comments

    def get_comment_amount(self):
        if self.comments:
            return len(self.comments)
        else:
            ca = database.query( 'SELECT ' + commentTableColumns['relatedPost'] + \
                                 ' FROM ' + commentTable + ' WHERE ' + \
                                 commentTableColumns['relatedPost'] + '=%i' 
                                 %self.relatedPost )
            return len(ca)

class NewComment():

    def __init__(self, form):
        form = inputverification.NewCommentForm( form )
        if not form.verify:
            raise exceptions.CantCreateNewComment

        self.comment = form.comment
        self.relatedPost = form.relatedPost
        self.date = time.strftime('%d.%m.%y')
        self.user = get_current_user().id
        if not self.user:
            raise exceptions.NoUserLoggedIn

    def safe(self):
        database.commit( commentTable, [commentTableColumns['comment'], \
                                        commentTableColumns['relatedPost'], \
                                        commentTableColumns['user'], \
                                        commentTableColumns['date']], \
                         [self.comment, self.relatedPost, self.user, self.date] )