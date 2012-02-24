# -*- coding: UTF-8 -*-

from blackboard import app
from flaskext.login import login_required
import views
import admin

# urls
@app.route('/')
@login_required
def index():
    return views.index()

@app.route('/login/', methods=['GET', 'POST'])
def login():
    return views.login()

@app.route('/logout/')
def logout():
    return views.logout()

@app.route('/register/', methods=['GET', 'POST'])
def register():
    return views.register()

@app.route('/user/<username>/')
@login_required
def userpage(username):
    return views.userpage(username)

@app.route('/user/settings/')
@login_required
def usersettings():
    return views.usersettings()

@app.route('/user/settings/<change>/', methods=['POST'])
@login_required
def changesettings(change):
    return views.changesetting(change)

@app.route('/user/settings/avatar/del/', methods=['GET'])
@login_required
def delavatar():
    return views.changesetting('delavatar')

@app.route('/post/new/<ctype>/')
@login_required
def newpost(ctype):
    return views.newpost(ctype)

@app.route('/post/add/', methods=['POST'])
@login_required
def add_entry():
    return views.addpost()

@app.route('/posts/<int:id>/')
@login_required
def getpost(id):
    return views.getpost(id)

@app.route('/posts/<filter>/')
@login_required
def getposts(filter):
    return views.getposts(filter)

@app.route('/posts/<filter>/<int:page>/')
@login_required
def getposts_p(filter, page):
    return views.getposts(filter, page)

@app.route('/posts/user/<username>/')
@login_required
def getuserpost(username):
    return views.getuserposts(username)

@app.route('/posts/user/<username>/<int:page>/')
@login_required
def getuserpost_p(username, page):
    return views.getuserposts(username, page)

@app.route('/posts/all/list/')
@login_required
def getallposts():
    return views.getminimalpostlist()

@app.route('/page/<int:nr>/')
@login_required
def getpage(nr):
    return views.getpage(nr)

@app.route('/comment/add/', methods=['POST'])
@login_required
def addcomment():
    return views.addcomment()

@app.route('/upload/<utype>/', methods=['POST'])
@login_required
def upload(utype):
    return views.handle_upload(utype)

@app.route('/public/<public_post_id>/', methods=['GET'])
def public(public_post_id):
    return views.public_link(public_post_id)

@app.route('/p/<public_post_id>/', methods=['GET'])
def p(public_post_id):
    return views.public_link(public_post_id)

# Admin sites
@app.route('/admin/')
@login_required
def admin_index():
    return admin.index()

@app.route('/admin/user/')
@login_required
def admin_user():
    return admin.user()

@app.route('/admin/user/<int:id>/')
@login_required
def admin_user_detail(id):
    return admin.userdetail(id)

@app.route('/admin/user/<int:id>/del')
@login_required
def admin_user_del(id):
    return admin.deluser(id)

@app.route('/admin/user/<int:id>/activate/')
@login_required
def admin_user_activate(id):
    return admin.activate(id)

@app.route('/admin/user/<int:id>/setpw/', methods=['POST'])
@login_required
def admin_setpw(id):
    return admin.setpw(id)

@app.route('/admin/posts/')
@login_required
def admin_posts():
    return admin.post(None)

@app.route('/admin/posts/<int:id>/')
@login_required
def admin_post_show(id):
    return admin.post(id)

@app.route('/admin/posts/<int:id>/del/')
@login_required
def admin_post_delete(id):
    return admin.delpost(id)

@app.route('/admin/posts/<int:id>/set_public/')
@login_required
def admin_post_set_public(id):
    return admin.setpublic(id)

# Facebook integration
@app.route('/facebook/oauth/')
@login_required
def facebook_authentication():
    return views.facebook_authentication()

@app.route('/facebook/response/')
@login_required
def facebook_response():
    return views.facebook_handle_response()

@app.route('/facebook/response/<action>/<arg>/')
@login_required
def facebook_response_(action, arg):
    return views.facebook_handle_response(action, arg)

@app.route('/facebook/push_post/<post_id>/')
@login_required
def facebook_push_post(post_id):
    return views.facebook_push_post(post_id)

