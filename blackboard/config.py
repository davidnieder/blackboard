# -*- coding: utf-8 -*-

import os
from ConfigParser import SafeConfigParser


path = os.path.dirname(__file__)
config_file = path + '/config.cfg'

def get(setting, type=None):
    parser = SafeConfigParser()
    parser.read(config_file)

    if type is bool:
        return parser.getboolean('USER', setting)
    elif type is int:
        return parser.getint('USER', setting)
    elif type is list or type is tuple:
        s = parser.get('USER', setting)
        s = s.split(',')
        if not s[-1]:
            s = s[:-1]
        if type is tuple:
            return tuple(s)
        return s
    else:
        return parser.get('USER', setting)

def set(setting, value):
    parser = SafeConfigParser()
    parser.read(config_file)

    parser.set('USER', setting, value)
    f = open(config_file, 'w')
    parser.write(f)
    f.close()

def options():
    parser = SafeConfigParser()
    parser.read(config_file)

    return parser.options('USER')

