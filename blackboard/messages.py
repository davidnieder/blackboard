# -*- coding: utf-8 -*-


# views.py
# login messages
logged_in = u'You have successfully logged in'
logged_out = u'You have succesfully logged out'
user_not_activated = u'Your account was not activated by an Administrator yet'
invalid_credentials = u'You have entered either a wrong user name or a ' + \
                      u'wrong password'
# register messages
username_already_exists = u'The entered user name already exists'
registered_and_logged_in = u'Successfully registert: you are now logged in'
registered_and_deactivated = u'Successfully registert: your account has ' + \
                             u'to be activated by an Administrator'
register_error = u'An error occured during registration'
register_field_error = u'Please fill in all fields'
# new post, comment messages
post_created = u'New post successfully created'
post_error = u'Your post could not be created'
post_edited = u'Your post was edited'
post_edit_error = u'Yout post could not be edited'
comment_error = u'Your comment could not be created'


# usersettings.py
wrong_password = u'The given password was not correct'
changed_password = u'You have successfully changed your password'
changed_email = u'You have successfully changed your email address'
changed_setting = u'Setting successfully changed'
changed_template = u'Your template setting was changed'
changed_facebook_integration = u'Changed facebook integration setting'


# facebook.py
fb_access_denied = u'Could not post on facebook: access denied'
fb_invalid_post_id = u'Could not post on facebook: post id is invalid'
fb_post_is_private = u'Could not post on facebook: post is not public'
fb_invalid_post_type = u'Could not post on facebook: post type is invalid'
fb_error_returned = u'Could not post on facebook: an error occurred'
fb_successfully_posted = u'Post successfully pushed to your facebook wall'


# admin.py
no_admin_access = u'You have no authorization to enter this page'
user_deleted = u'The user was deleted'
user_activated = u'The user was activated'
user_deactivated = u'The user was deactivated'
user_not_found = u'The user could not be found'
user_set_password = u'The password was successfully set'
post_not_found = u'The post could not be found'
post_deleted = u'The post was deleted'
post_marked_public = u'The post was marked as public'
post_marked_private = u'The post was marked as private'
comment_not_found = u'The comment does not exist'
comment_deleted = u'The comment was deleted'


# setup.py
invalid_database_uri = u'The entered database uri is invalid'
passwords_dont_match = u'The entered passwords do not match'
setup_finished = u'Setup successfully finished'


# login required message
login_required = u'Please login in to view this page'

