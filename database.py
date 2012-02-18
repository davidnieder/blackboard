import sqlite3, time
from config import DATABASE, DBSCHEMA
from flask import g, flash

import exceptions

def opendb():
    g.db = connectdb()

def closedb():
    if hasattr(g, 'db'):
        g.db.close()

def connectdb():
    return sqlite3.connect(DATABASE)

def initdb():
    import initdb
    initdb.init_db()

def adduser(name, password, email, admin, active, avatar, style, template, lastlogin, \
            postspersite, emailnotification, rememberme):
    g.db.execute('insert into users (name, password, email, admin, active, avatar, \
                style, template, lastlogin, postspersite, emailnotification, rememberme) \
                values  (?,?,?,?,?,?,?,?,?,?,?,?)',
                [name, password, email, admin, active, avatar, style, template, lastlogin, \
                 postspersite, emailnotification, rememberme])
    g.db.commit()

def delpost(id):
    g.db.execute('delete from posts where id=%i' %id)
    g.db.commit()
    return True

def getuser(user):
    opendb()
    if type(user) == str or type(user) == unicode:    
        cursor = g.db.execute('select id, name, password, email, admin, active, avatar, \
                                style, template, lastlogin, postspersite from users where \
                                name=\'%s\'' % user)
    else:
        cursor = g.db.execute('select id, name, password, email, admin, active, avatar, \
                                style, template, lastlogin, postspersite \
                                from users where id=%i' % user)
    tup = cursor.fetchone()
    if tup:
        return dict(id=tup[0], name=tup[1], password=tup[2], email=tup[3], \
                    admin=tup[4], active=tup[5], avatar=tup[6], style=tup[7], \
                    template=tup[8], lastlogin=tup[9], postspersite=tup[10])
    return None

def getusername( id ):
    cursor = g.db.execute('select name from users where id=%i' %id)
    username = cursor.fetchone()

    return username[0] if username else None

def getuserid( username ):
    cursor = g.db.execute('select id from users where name=\'%s\'' %username)
    userid = cursor.fetchone()[0]

    if not userid:
        raise exeptions.NoSuchUser()
    return userid

def getusers():
    cursor = g.db.execute('select * from users')
    userlist = cursor.fetchall()

    users = []
    for ut in userlist:
        users += [dict(id=ut[0], name=ut[1], email=ut[3], admin=ut[4], active=ut[5], \
                        lastlogin=ut[6])]
    return users

def deluser(id):
    g.db.execute('delete from users where id=%i' %id)
    g.db.commit()

def activateuser(id, active):
    g.db.execute('update users set active=%i where id=%i' %(active, id))
    g.db.commit()

def updatelogindate(userid):
    g.db.execute('update users set lastlogin=\'%s\' where id=%i' \
                %( time.strftime('%d.%m.%y'), userid))
    g.db.commit()

def updatesetting(userid, column, value):
    if value == int:
        g.db.execute('update users set \'%s\'=%i where id=%i' \
                    %(column, value, userid))
    else:
        g.db.execute('update users set \'%s\'=\'%s\' where id=%i' \
                    %(column, value, userid))
    g.db.commit()

def query( q ):
    cursor = g.db.execute( q )
    # patch row_factory
    cursor.row_factory = dict_factory
    return cursor.fetchall()

def commit( table, columnList, valueList ):
    columns = ''
    columnAmount = ''

    for column in columnList:
        columns += column + ', '
        columnAmount += '?,'
    columns = columns[:-2]
    columnAmount = columnAmount[:-1]

    if len(columnList) != len(valueList):
        raise exceptions.ColumnAndValueListDontMatch

    g.db.execute('INSERT INTO ' + table + ' (' + columns + ')' + ' VALUES ' + \
                 '(' + columnAmount + ')', valueList)
    g.db.commit()

    cursor = g.db.execute('SELECT last_insert_rowid()')
    return cursor.fetchone()

def delete( table, column, condition ):
    pass

def check_if_entry_exists( table, column, value ):
    cursor = g.db.execute('SELECT * FROM ' + table + ' WHERE ' + \
                          column + '=' + str(value) + ' LIMIT 1')
    entry = cursor.fetchone()

    return True if entry else False


def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

