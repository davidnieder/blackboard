# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime

import inputvalidation
import exceptions
import comment
import user
from database import db, Posts as DBPosts


class Posts():

    def __init__(self, username=None, user_id=None, page=1, post_filter=None,
                 id_list=None, only_public=False):

        self.username = username
        self.user_id = user_id
        self.page = page
        self.post_filter = post_filter
        self.id_list = id_list
        self.only_public = only_public

        self.posts_per_page = user.get_posts_per_page()

        if self.username or self.user_id:
            # get user posts
            if self.username:
            # get user_id from username
                self.user_id = user.get_user_id_from_name(self.username)

            self.post_list = DBPosts.query. \
                             filter_by(user_id=self.user_id). \
                             order_by(DBPosts.id.desc()). \
                             limit(self.posts_per_page). \
                             offset((self.page-1)*self.posts_per_page). \
                             all()

        elif self.post_filter:
            # filtered view e.g. /posts/audio/
            if self.post_filter in ['audio', 'video', 'image', 'text', 'link']:
                self.post_list = DBPosts.query. \
                                 filter_by(content_type=self.post_filter). \
                                 order_by(DBPosts.id.desc()). \
                                 limit(self.posts_per_page). \
                                 offset((self.page-1)*self.posts_per_page). \
                                 all()
            # filter by date
            elif self.post_filter:

                self.post_list = DBPosts.query. \
                                 filter(DBPosts.time.startswith(self.post_filter)). \
                                 order_by(DBPosts.id.desc()). \
                                 limit(self.posts_per_page). \
                                 offset((self.page-1)*self.posts_per_page). \
                                 all()
            else:
                self.post_list = []

        elif self.id_list == 'all':
            # get all posts
            self.post_list = DBPosts.query.order_by(DBPosts.id.desc()).all()

        elif self.id_list:
            # get some specified posts
            pass

        elif self.only_public:
            # get public index page
            self.post_list = DBPosts.query. \
                             filter_by(is_public=True). \
                             order_by(DBPosts.id.desc()). \
                             limit(self.posts_per_page). \
                             offset((self.page-1)*self.posts_per_page). \
                             all()

        else:
            # get index page
            self.post_list = DBPosts.query. \
                             order_by(DBPosts.id.desc()). \
                             limit(self.posts_per_page). \
                             offset((self.page-1)*self.posts_per_page). \
                             all()

    def get_posts(self):
        return self.post_list


class Post():

    def __init__(self, post_id=None, public_id=None):

        if post_id:
            self.id = post_id
            self.db_post = DBPosts.query.filter_by(id=self.id).first()
        elif public_id:
            self.public_id = public_id
            self.db_post = DBPosts.query.filter_by(public_id=self.public_id,
                           is_public=True).first()
        else:
            #no id was given
            self.db_post = None

        if self.db_post:
            self.id = self.db_post.id
            self.title = self.db_post.title
            self.content = self.db_post.content
            self.comment = self.db_post.comment
            self.content_type = self.db_post.content_type
            self.time = self.db_post.time
            self.is_public = self.db_post.is_public
            self.public_id = self.db_post.public_id
            self.comments = self.db_post.comments
            self.user_id = self.db_post.user_id
            self.user = self.db_post.user
        else:
            self.id = None

    def delete(self):
        db.session.delete(self.db_post)
        db.session.commit()        

    def update(self, attr, value):
        if hasattr(self.db_post, attr):
            setattr(self.db_post, attr, value)

            db.session.add(self.db_post)
            db.session.commit()

    def get_post(self):
        if not self.id:
            return None
        else:
            return dict(id=self.id, title=self.title, content=self.content,
                        comment=self.comment, content_type=self.content_type,
                        time=self.time, is_public=self.is_public,
                        public_id=self.public_id, comments=self.comments,
                        user=self.user)

    def set_public(self):
        if not self.public_id:
            while True:
                md5_hash = hashlib.md5()
                md5_hash.update(str(self.time)+str(self.id))
                public_id = md5_hash.hexdigest()[:5]

                if DBPosts.query.filter_by(public_id=public_id).first():
                    continue
                else:
                    self.public_id = public_id
                    self.db_post.public_id = public_id
                    break

        self.is_public = True
        self.db_post.is_public = True

        db.session.add(self.db_post)
        db.session.commit()


class NewPost():

    def __init__(self, form):
        try:
            validate = inputvalidation.NewPostForm(form)
            self.new_post = validate.validated_form
        except:
            raise exceptions.CantValidateForm

        self.title = self.new_post['title'] if self.new_post['title'] \
                                            else ''
        self.content = self.new_post['content']
        self.comment = self.new_post['comment'] if self.new_post['comment'] \
                                                else ''
        self.content_type = self.new_post['content_type']
        self.time = datetime.now()
        self.user = user.get_current_db_user()

        if self.new_post['is_public']:
            self.is_public = True
            while True:
                md5_hash = hashlib.md5()
                md5_hash.update(str(self.time)+str(self.id))
                public_id = md5_hash.hexdigest()[:5]

                if DBPosts.query.filter_by(public_id=public_id).first():
                    continue
                else:
                    self.public_id = public_id
                    break
        else:
            self.is_public = False
            self.public_id = None

    def safe(self):
        # create post object
        self.db_post = DBPosts( title = self.title,
                                content = self.content,
                                comment = self.comment,
                                content_type = self.content_type,
                                time = self.time,
                                user = self.user,
                                is_public = self.is_public,
                                public_id = self.public_id )

        # commit to database
        db.session.add(self.db_post)
        db.session.commit()

    def get_id(self):
        return self.db_post.id


def check_if_post_exists(post_id):
    if DBPosts.query.filter_by(id=post_id).first():
        return True
    return False

def check_if_public_post_exists(public_id):
    if DBPosts.query.filter_by(public_id=public_id).first():
        return True
    return False

