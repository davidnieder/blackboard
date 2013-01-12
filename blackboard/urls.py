# -*- coding: utf-8 -*-

from base import app
import views, admin, facebook, setup


# index
app.add_url_rule('/', view_func=views.index)


# login, logout, register
app.add_url_rule('/login/', view_func=views.login, methods=['GET', 'POST'])

app.add_url_rule('/logout/', view_func=views.logout)

app.add_url_rule('/register/', view_func=views.register,
                 methods=['GET', 'POST'])


# user page, settings
app.add_url_rule('/user/<name>/', view_func=views.user_page)

app.add_url_rule('/user/settings/', view_func=views.user_settings,
                 methods=['GET', 'POST'])


# post views
app.add_url_rule('/posts/<int:post_id>/', view_func=views.get_post)

app.add_url_rule('/posts/<filter>/', view_func=views.get_posts)

app.add_url_rule('/posts/<filter>/<int:page_number>/',
                 view_func=views.get_posts)

app.add_url_rule('/posts/user/<username>/', view_func=views.get_user_posts)

app.add_url_rule('/posts/user/<username>/<int:page_number>/',
                 view_func=views.get_user_posts)

app.add_url_rule('/posts/all/list/', view_func=views.get_minimal_post_list)

app.add_url_rule('/page/<int:page_number>/', view_func=views.get_page)


# new post, comment
app.add_url_rule('/post/new/<post_type>/', view_func=views.new_post)

app.add_url_rule('/post/add/', view_func=views.add_post, methods=['POST'])

app.add_url_rule('/comment/add/', view_func=views.add_comment,
                 methods=['POST'])


# uploads
app.add_url_rule('/upload/<file_type>/', view_func=views.handle_upload,
                 methods=['POST'])


# public pages
app.add_url_rule('/public/', view_func=views.public_index)

app.add_url_rule('/public/page/<int:page_number>/', view_func=views.public_page)

app.add_url_rule('/public/<public_post_id>/', view_func=views.public_post)

app.add_url_rule('/public/category/<filter>/', view_func=views.public_posts)

app.add_url_rule('/public/category/<filter>/<int:page_number>/',
                 view_func=views.public_posts)

app.add_url_rule('/public/user/<username>/', view_func=views.public_user_posts)

app.add_url_rule('/public/user/<username>/<int:page_number>/',
                 view_func=views.public_user_posts)

app.add_url_rule('/public/post/random/', view_func=views.public_random_post)

# admin pages
app.add_url_rule('/admin/', 'admin_index', view_func=admin.index)

app.add_url_rule('/admin/settings/', 'admin_settings',
                 view_func=admin.settings, methods=['GET', 'POST'])

app.add_url_rule('/admin/user/', 'admin_user', view_func=admin.user,
                 methods=['GET', 'POST'])

app.add_url_rule('/admin/user/<int:id>/', 'admin_user_details',
                 view_func=admin.user_details)

app.add_url_rule('/admin/post/', 'admin_post', view_func=admin.post,
                 methods=['GET', 'POST'])

app.add_url_rule('/admin/post/<int:id>/', 'admin_post_id', view_func=admin.post)

app.add_url_rule('/admin/comment/', 'admin_comment',
                 view_func=admin.comment, methods=['GET', 'POST'])

app.add_url_rule('/admin/comment/<int:id>/', 'admin_comment',
                 view_func=admin.comment)


# facebook integration
app.add_url_rule('/facebook/authorization/', 'facebook_authorization',
                 view_func=facebook.authorization)

app.add_url_rule('/facebook/authorized/', 'facebook_authorized',
                 view_func=facebook.authorized)

app.add_url_rule('/facebook/authorize_and_post/<post_id>/',
                 'facebook_authorize_and_post',
                 view_func=facebook.authorize_and_post)

app.add_url_rule('/facebook/push_post/<post_id>/', 'facebook_push_post',
                 view_func=facebook.push_post)

# atom feeds
app.add_url_rule('/feed/', 'feed', view_func=views.feed)

app.add_url_rule('/public/feed/', 'public_feed', view_func=views.public_feed)

