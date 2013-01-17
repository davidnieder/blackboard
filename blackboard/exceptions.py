# -*- coding: utf-8 -*-
# whole use of exceptions in blackboard needs to be rethought

class BlackboardException(Exception):
    '''Base class for exceptions in Blackboard'''
    def __init__(self, error_message=None, internal_error_message=None):
        self.error_message = error_message
        self.internal_error_message = internal_error_message

    def __str__(self):
        return self.error_message

# User
class UserAlreadyExists(BlackboardException):
    '''
    This Exception is raised if a username already exists in the Database
    '''
class NoSuchUser(BlackboardException):
    '''
    This Exception is raised if a requested user does not exist
    '''
class NoUserLoggedIn(BlackboardException):
    '''
    Thrown if in a context of a request no user is logged in
    '''

# Upload
class NoSuchUploadSet(BlackboardException):
    '''
    This Exception is raised if a UploadSet does not exist
    '''
class CantCreateUploadSet(BlackboardException):
    '''
    This Exception is raised if an UploadSet could not be created
    '''
class UploadFailed(BlackboardException):
    '''
    Raised if an Upload fails
    '''

# Post
class CantCreateNewPost(BlackboardException):
    '''
    Raised if the creation of a new post fails
    '''
class NoPublicPostId(BlackboardException):
    '''
    Raised if a given public post id has no post id equivalent
    '''
class NoSuchPostId(BlackboardException):
    '''
    Raised if a Post id does not exist
    '''

# Comment
class CantCreateNewComment(BlackboardException):
    '''
    Raised if the creation of a new comment failes
    '''

# User settings
class NoSuchUserSetting(BlackboardException):
    '''
    Raised if a setting should be changed that does not exist
    '''

# Input validation
class CantValidateForm(BlackboardException):
    '''
    Raised if input validation fails
    '''

# Facebook integration
class AppIsNotAuthenticated(BlackboardException):
    '''
    Raised if the facebook app is not authenticated
    '''
class CantPostToWall(BlackboardException):
    '''
    Raised if a post to the facebook wall fails
    '''
class AuthenticationFailed(BlackboardException):
    '''
    Raised if the authentication procedure has failed
    '''

