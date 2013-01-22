# -*- coding: utf-8 -*-

import uuid
import random
from datetime import datetime

import inputvalidation
import exceptions
import comment
import user
import config
from database import db, Posts as DBPosts


post_categories = config.get('post_categories', list)

class Posts():

    def __init__(self, username=None, user_id=None, page=1, post_filter=None,
                 id_list=None, only_public=False, post_amount=None):

        self.username = username
        self.user_id = user_id
        self.page = page
        self.post_filter = post_filter
        self.id_list = id_list
        self.only_public = only_public

        self.posts_per_page = post_amount if post_amount else \
                              user.get_posts_per_page()

        self.offset = (self.page-1)*self.posts_per_page

        # get post query object
        query = DBPosts.query

        if self.id_list == 'all':
            # get all posts and return
            self.post_list = query.order_by(DBPosts.id.desc()).all()
            return

        if self.username and not self.user_id:
            # get user id
            self.user_id = user.get_user_id_from_name(self.username)
            # filter posts py user
            query = query.filter_by(user_id=self.user_id)

        if self.post_filter:
            if self.post_filter in post_categories:
                # filter by categories
                query = query.filter_by(content_type=self.post_filter)
            else:
                # filter by date
                query = query.filter(DBPosts.time.startswith(self.post_filter))

        if self.only_public:
            # only public posts
            query = query.filter_by(is_public=True)

        # set order
        query = query.order_by(DBPosts.id.desc())
        # set limit
        query = query.limit(self.posts_per_page)
        # set offset
        query = query.offset(self.offset)

        # query database
        self.post_list = query.all()


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
            # no id was given
            self.db_post = None

        if self.db_post:
            self.id = self.db_post.id
            self.title = self.db_post.title
            self.content = self.db_post.content
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

    def edit(self, new_post):
        self.title = new_post.title
        self.content = new_post.content
        self.content_type = new_post.content
        self.is_public = new_post.is_public
        self.db_post.title = new_post.title
        self.db_post.content = new_post.content
        self.db_post.content_type = new_post.content_type
        self.db_post.is_public = new_post.is_public

        if self.is_public and not self.public_id:
            self.public_id = generate_public_id(self.time, self.user.id)
            self.db_post.public_id = self.public_id
            new_post.public_id = self.public_id

        new_post.id = self.id

        db.session.add(self.db_post)
        db.session.commit()

    def get_post(self):
        if not self.id:
            return None
        else:
            return dict(id=self.id, title=self.title, content=self.content,
                        content_type=self.content_type, time=self.time,
                        is_public=self.is_public, public_id=self.public_id,
                        comments=self.comments, user=self.user)

    def set_public(self):
        if not self.public_id:
            self.public_id = generate_public_id(self.time, self.user.id)
            self.db_post.public_id = self.public_id

        self.is_public = True
        self.db_post.is_public = True

        db.session.add(self.db_post)
        db.session.commit()


class NewPost():

    def __init__(self, form):
        try:
            post_form = inputvalidation.ValidatePostForm(form)
        except exceptions.CantValidateForm:
            raise exceptions.CantCreateNewPost

        self.title = post_form.title
        self.content = post_form.content
        self.content_type = post_form.category
        self.is_public = post_form.is_public

        self.time = datetime.now()
        self.user = user.get_current_user()

        # generate public id
        if self.is_public:
            self.public_id = generate_public_id(self.time, self.user.id)
        else:
            self.is_public = False
            self.public_id = None

    def save(self):
        # create post object
        self.db_post = DBPosts(title = self.title,
                               content = self.content,
                               content_type = self.content_type,
                               time = self.time,
                               user = self.user.get_db_obj(),
                               is_public = self.is_public,
                               public_id = self.public_id)

        # commit to database
        db.session.add(self.db_post)
        db.session.commit()

        # now this post has an id
        self.id = self.db_post.id

    def generate_public_id(self):
        while True:
            md5_hash = hashlib.md5()
            md5_hash.update(str(self.time)+str(self.user.id))
            public_id = md5_hash.hexdigest()[:5]

            if DBPosts.query.filter_by(public_id=public_id).first():
                continue
            else:
                self.public_id = public_id
                break

    def get_id(self):
        return self.id


def generate_public_id(time, user_id):
    while True:
        public_id = uuid.uuid4().hex[:5]
        if DBPosts.query.filter_by(public_id=public_id).first():
            continue
        else:
            return public_id

def check_if_post_exists(post_id):
    if DBPosts.query.filter_by(id=post_id).first():
        return True
    return False

def check_if_public_post_exists(public_id):
    if DBPosts.query.filter_by(public_id=public_id).first():
        return True
    return False

def get_random_post():
    row_count = DBPosts.query.filter_by(is_public=True).count()
    rand = random.randrange(1, row_count+1)
    row = DBPosts.query.get(rand)

    post = Post(post_id=row.id)
    return post.get_post()

