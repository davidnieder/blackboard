import sqlite3, time
from config import DATABASE, DBSCHEMA, POSTSPERSITE
from flask import g, flash

import exceptions

contentkey = {  'text': 1,  1: 'text',
                'image': 2, 2: 'image',
                'video': 3, 3: 'video',
                'link': 4,  4: 'link',
                'audio': 5,  5: 'audio'   }

def opendb():
    g.db = connectdb()

def closedb():
    if hasattr(g, 'db'):
        g.db.close()
    else:
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

def addentry( form, user ):
    if form['contenttype'] == 'text':
        if form['content']:
            g.db.execute('insert into posts (title, text, contenttype, time, user) \
                        values (?,?,?,?,?)',
                        [form['title'], form['content'], contentkey['text'], \
                        time.strftime('%d.%m.%y'), user])
            g.db.commit()

    elif form['contenttype'] == 'image':
        if form['link']:
            g.db.execute('insert into posts (title, text, url, contenttype, time, user) \
                        values (?,?,?,?,?,?)',
                        [form['title'], form['comment'], form['link'], contentkey['image'], \
                        time.strftime('%d.%m.%y'), user])
            g.db.commit()
        

    elif form['contenttype'] == 'video':
        if form['code']:
            g.db.execute('insert into posts (title, text, code, contenttype, time, user) \
                        values (?,?,?,?,?,?)',
                        [form['title'], form['comment'], form['code'], contentkey['video'], \
                        time.strftime('%d.%m.%y'), user])
            g.db.commit()

    elif form['contenttype'] == 'link':
        if form['link']:
            g.db.execute('insert into posts (title, text, url, contenttype, time, user) \
                        values (?,?,?,?,?,?)',
                        [form['title'], form['comment'], form['link'], contentkey['link'], \
                        time.strftime('%d.%m.%y'), user])
            g.db.commit()

    elif form['contenttype'] == 'audio':
        if form['code']:
            g.db.execute('insert into posts (title, text, code, contenttype, time, user) \
                        values (?,?,?,?,?,?)',
                        [form['title'], form['comment'], form['code'], contentkey['audio'], \
                        time.strftime('%d.%m.%y'), user])
            g.db.commit()
    else:
        pass

def getpost(id):
    cursor = g.db.execute('select title, text, url, code, time, contenttype, id, user \
                            from posts where id=%i' %id)
    tup = cursor.fetchone()
    if tup:
        return dict(title=tup[0], text=tup[1], url=tup[2], code=tup[3], \
                    date=tup[4], contenttype=contentkey[tup[5]], id=tup[6], \
                    user=tup[7])
    else:
        return []

def getposts(filter, frompost=0, topost=POSTSPERSITE):
    if filter in ['text', 'link', 'image', 'audio', 'video']:
        cursor = g.db.execute('select title, text, url, code, time, contenttype, id, user \
                                from posts where contenttype=%i order by id desc' \
                                %contentkey[filter])
    else:
        cursor = g.db.execute('select title, text, url, code, time, contenttype, id, user \
                                from posts where time=\'%s\' order by id desc' % filter )

    posts = []
    for tup in cursor.fetchall()[frompost:topost]:
        posts += [dict(title=tup[0], text=tup[1], url=tup[2], code=tup[3], date=tup[4], \
                    contenttype=contentkey[tup[5]], id=tup[6], user=tup[7])]
    return posts

def delpost(id):
    g.db.execute('delete from posts where id=%i' %id)
    g.db.commit()
    return True

def getuserposts(username, frompost=0, topost=POSTSPERSITE):
    cursor = g.db.execute('select title, text, url, code, time, contenttype, id, user \
                                from posts where user=\'%s\' order by id desc' %username)
    posts = []
    for tup in cursor.fetchall()[frompost:topost]:
        posts += [dict(title=tup[0], text=tup[1], url=tup[2], code=tup[3], date=tup[4], \
                    contenttype=contentkey[tup[5]], id=tup[6], user=tup[7])]
    return posts

def getentries(i=POSTSPERSITE, frompost=0, topost=POSTSPERSITE):
    cursor = g.db.execute('select title, text, url, code, time, contenttype, id, user from \
                            posts order by id desc')

    posts = []
    for tup in cursor.fetchmany(i)[frompost:topost]:
        #Get Avatar
        cu = g.db.execute('select avatar from users where name=\'%s\'' %tup[7])
        avatar = cu.fetchone()[0]

        if tup[5] == contentkey['text']:
            posts += [dict(title=tup[0], text=tup[1], date=tup[4], contenttype='text', \
                        id=tup[6], user=tup[7], comments=getcommentamount(tup[6]), \
                        avatar=avatar)]

        elif tup[5] == contentkey['link'] or tup[5] == contentkey['image']:
            posts += [dict(title=tup[0], comment=tup[1], url=tup[2], date=tup[4], \
                        contenttype=contentkey[tup[5]], id=tup[6], user=tup[7], \
                        comments=getcommentamount(tup[6]), avatar=avatar)]

        elif tup[5] == contentkey['video'] or tup[5] == contentkey['audio']:
            posts += [dict(title=tup[0], comment=tup[1], code=tup[3], date=tup[4], \
                        contenttype=contentkey[tup[5]], id=tup[6], user=tup[7], \
                        comments=getcommentamount(tup[6]), avatar=avatar)]

    return posts

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

def addcomment(userid, comment, relatedpost):
    g.db.execute('insert into comments (userid, comment, relatedpost, time) values \
                    (?,?,?,?)', [userid, comment, relatedpost, time.strftime('%d.%m.%y')])
    g.db.commit()

def getcomment( id ):
    cursor = g.db.execute('select userid, comment, relatedpost, time from comments \
                            where id=%i' %id)
    tup = cursor.fetchone()
    return dict(userid=tup[0], comment=tup[1], relatedpost=tup[2], time=tup[3], \
                username=getusername(tup[0]))

def getcomments( relatedpost ):
    cursor = g.db.execute('select userid, comment, time from comments where \
                           relatedpost=\'%s\' order by id desc' %relatedpost)
    commentlist = cursor.fetchall()
    comments = []
    for tup in commentlist:
        comments += [dict(userid=tup[0], comment=tup[1], time=tup[2], \
                    username=getusername(tup[0]))]
    return comments

def getcommentamount( relatedpost ):
    cursor = g.db.execute('select comment from comments where relatedpost=%i' %relatedpost)
    comments = cursor.fetchall()
    return len(comments)

