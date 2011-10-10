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
    return views.changesettings(change)

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

@app.route('/page/<int:nr>/')
@login_required
def getpage(nr):
    return views.getpage(nr)

@app.route('/comment/add/', methods=['POST'])
@login_required
def addcomment():
    return views.addcomment()

# Admin sites
@app.route('/admin/')
def admin_index():
    return admin.index()

@app.route('/admin/user/')
def admin_user():
    return admin.user()

@app.route('/admin/user/<int:id>/')
def admin_user_detail(id):
    return admin.userdetail(id)

@app.route('/admin/user/<int:id>/del')
def admin_user_del(id):
    return admin.deluser(id)

@app.route('/admin/user/<int:id>/activate/')
def admin_user_activate(id):
    return admin.activate(id)

@app.route('/admin/user/<int:id>/setpw/', methods=['POST'])
def admin_setpw(id):
    return admin.setpw(id)

@app.route('/admin/posts/')
def admin_posts():
    return admin.post(None)

@app.route('/admin/posts/<int:id>/')
def admin_post_show(id):
    return admin.post(id)

@app.route('/admin/posts/<int:id>/del/')
def admin_post_delete(id):
    return admin.delpost(id)
