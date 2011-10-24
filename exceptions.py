# User
class UserAlreadyExists(Exception):
    '''
    This Exception is raised if a username already exists in the Database
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
