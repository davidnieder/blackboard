import database, exceptions
from flaskext.login import login_user, logout_user, current_user
from config import ACCOUNTACTIVATION, POSTSPERSITE

class User:
    def __init__(self, username=None, id=None):
        self.username = username
        self.id = id

        fromdb = self.query()
        if not fromdb:
            self.username = None
            self.password = None
            self.id = None
            self.email = None
            self.admin = False
            self.active = False
            self.avatar = None
            self.style = None
            self.template = None
            self.lastlogin = None
            self.postspersite = None
        else:
            self.username = fromdb['name']
            self.password = fromdb['password']
            self.id = fromdb['id']
            self.email = fromdb['email']
            self.admin = True if fromdb['admin'] else False
            self.active = True if fromdb['active'] else False
            self.avatar = fromdb['avatar']
            self.style = fromdb['style']
            self.template = fromdb['template']
            self.lastlogin = fromdb['lastlogin']
            self.postspersite = fromdb['postspersite']

        self.authenticated = False

    def __delete__(self):
        pass

    def authenticate(self, password):
        return True if password==self.password else False

    def query(self):
        q = self.username if self.username else self.id
        return database.getuser(q)    

    def is_authenticated(self):
        return True 

    def is_active(self):
        return True if self.active else False

    def is_anonymous(self):
        return False;

    def get_id(self):
        return unicode(self.id);

    def set_avatar(self, url):
        database.updatesetting(self.id, 'avatar', url)

class NewUser(User):
    def __init__(self, username, password, email):
        User.__init__(self, username=username)

        if self.username:
            raise exceptions.UserAlreadyExists()
        else:
            self.username = username
            self.password = password
            self.email = email

            self.create()

    def create(self):
        self.active = 0 if ACCOUNTACTIVATION else 1
        database.adduser(name=self.username, password=self.password, \
                        email=self.email, admin=0, active=self.active, avatar='null', \
                        style='default', template='default', lastlogin='', \
                        postspersite=POSTSPERSITE, emailnotification=0, rememberme=0)
        # Get the new User ID
        self.id = database.getuserid( self.username )

def get(userid):
    '''Returns User-object or None'''
    u = User(id=int(userid))
    return u if u.username else None

def get_current_user()
    '''Returns the current, logged-in user or None'''
    try:
        return current_user
    except:
        return None

