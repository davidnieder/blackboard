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
class UploadFailed(Exception):
    '''
    Raised if an Upload fails
    '''

# Post
class CantCreateNewPost(Exception):
    '''
    Raised if the creation of a new post fails
    '''

class NoPublicPostId(Exception):
    '''
    Raised if a given public post id has no post id equivalent
    '''

class NoSuchPostId(Exception):
    '''
    Raised if a Post id does not exist
    '''

# Comment
class CantCreateNewComment(Exception):
    '''
    Raised if the creation of a new comment failes
    '''

# User settings
class NoSuchSetting(Exception):
    '''
    Raised if setting should be changed that does not exist
    '''

# Database
class ColumnAndValueListDontMatch(Exception):
    '''
    Raised if the parameters for a commit do not fit
    '''

# Input validation
class CantValidateForm(Exception):
    '''
    Raised if input validation fails
    '''

# Facebook integration
class AppIsNotAuthenticated(Exception):
    '''
    Raised if the facebook app is not authenticated
    '''

class CantPostToWall(Exception):
    '''
    Raised if a post to the facebook wall fails
    '''

class AuthenticationFailed(Exception):
    '''
    Raised if the authentication procedure has failed
    '''

