#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
    starts the development server
'''

# path to site-package where the libraries are installed
sitedir = '/usr/lib/python-blackboard-env/lib/python2.7/site-packages'


import site
site.addsitedir(sitedir)

from blackboard import app
app.run()

