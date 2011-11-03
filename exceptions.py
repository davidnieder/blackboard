# User
class UserAlreadyExists(Exception):
    '''
    This Exception is raised if a username already exists in the Database
    '''
class NoSuchUser(Exception):
    '''
    This Exception is raised if a requested user does not exist
    '''
class NoUserLoggedIn(Exception):
    '''
    Thrown if in a context of a request no user is logged in
    '''

# Upload
class NotSuchUploadSet(Exception):
    '''
    This Exception is raised if a UploadSet does not exist
    '''
class CantCreateUploadSet(Exception):
    '''
    This Exception is raised if an UploadSet could not be create
    '''

# Post
class CantCreateNewPost(Exception):
    '''
    Raised if the creation of a new post fails
    '''

# Comment
class CantCreateNewComment(Exception):
    '''
    Raised if the creation of a new comment failes
    '''

# Database
class ColumnAndValueListDontMatch(Exception):
    '''
    Raised if the parameters for a commit do not fit
    '''
