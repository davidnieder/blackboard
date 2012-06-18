# -*- coding: utf-8 -*-
'''
    blackboard mod_wsgi example file
'''

# path to site-package folder where the libraries are installed
sitedir = '/usr/lib/python-blackboard-env/lib/python2.6/site-packages'


import site
site.addsitedir(sitedir)

from blackboard import app as application

