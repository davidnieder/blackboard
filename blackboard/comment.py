# -*- coding: utf-8 -*-

from datetime import datetime

import exceptions
import inputvalidation
import post

from user import get_current_user
from database import db, Comments as DBComments


class Comments():

    def __init__(self, post_id):
        self.post_id = post_id

        self.comment_list = DBComments.query. \
                            filter_by(related_post=self.post_id). \
                            order_by(DBComments.id.desc()). \
                            all()

    def get_comments(self):
        return self.comment_list

    def get_comment_amount(self):
        return len(self.comment_list)


class Comment():

    def __init__(self, id):
        self.db_comment = DBComments.query.filter_by(id=id).first()

        if self.db_comment:
            self.id = self.db_comment.id
            self.content = self.db_comment.content
            self.time = self.db_comment.time
            self.related_post = self.db_comment.related_post
            self.user = self.db_comment.user
        else:
            self.id = None

    def get_comment(self):
        if self.id:
            return dict(id=self.id, content=self.content, time=self.time,
                        related_post=self.related_post, user=self.user)
        else:
            return None

    def delete(self):
        db.session.delete(self.db_comment)
        db.session.commit()


class NewComment():

    def __init__(self, form):
        try:
            validate = inputvalidation.NewCommentForm(form)
            self.content = validate.get_content()
            self.related_post = validate.get_related_post_id()
        except:
            raise exceptions.CantCreateNewComment

        if not post.check_if_post_exists(self.related_post):
            raise exceptions.CantCreateNewComment

        self.time = datetime.utcnow()

        if not get_current_user():
            raise exceptions.CantCreateNewComment

        self.user_id = get_current_user().id

    def safe(self):
        self.db_comment = DBComments(
                                content = self.content,
                                time = self.time,
                                related_post = self.related_post,
                                user_id = self.user_id
                            )

        db.session.add(self.db_comment)
        db.session.commit()

        self.id = self.db_comment.id

