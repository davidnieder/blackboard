from contextlib import closing
import sqlite3
import os
import time

from config import DATABASE, DBSCHEMA

def backup():
    try:
        db = open( DATABASE )
    except:
        return

    backup = db.name + '.backup-' + time.strftime('%d.%m.%y-%H.%M')

    os.system('cp %s %s' %(db.name, backup))
    db.close()

def init_db():
    backup()

    with closing( sqlite3.connect( DATABASE ) ) as db:
        with open( DBSCHEMA ) as f:
            db.cursor().executescript(f.read())
        db.commit()
