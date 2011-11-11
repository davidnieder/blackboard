# -*- coding: UTF-8 -*-

# Database
DATABASE = '/var/www/blackboard/blackboard.sqlite3'
DBSCHEMA = 'dbschema.sql'

# Registration
# Muss ein account erst aktiviert werden?
ACCOUNTACTIVATION = True

# Posts pro Seite, default Wert
POSTSPERSITE = 5

# Ist das Blog komplett privat?
#PRIVATEBLOG = False

# Nachricht, die angezeigt wird, wenn ein Gast auf eine nur für
# registrierte Benutzer zugängliche Seite zugreifen möchte
LOGINREQUIREDMESSAGE = 'Bitte melde dich an um diese Seite zu sehen'

# Nachricht, wenn ein nicht priveligierter Benutzer auf die 
# Administrationsoberfläche zugreifen möchte
NOADMINACCESS = 'Du hast keine Berechtigung dieses Seite zu sehen'

# Verfügbare Templates und Styles hier eintragen
TEMPLATES = ['default']
STYLES = ['default']

# Uploads
# Wo sollen Uploads abgelegt werden?
UPLOADDESTINATION = '/var/www/blackboard/static/upload/'
# Erlaubte Dateiendungen
IMAGEEXTENSIONS = ('jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp')
FILEEXTENSIONS = ('gz', 'bz2', 'zip', 'tar', 'tgz', 'txz', '7z', 'rtf', 'odf', 'ods', \
                  'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'pdf')
AUDIOEXTENSIONS = ('mp3',)
# Maximale Dateigröße in Byte
MAXIMAGESIZE = 3145728 #  3MB
MAXFILESIZE = 10485760 # 10MB
MAXAUDIOSIZE =10485760 # 10MB
MAXAVATARSIZE = 512000 #500KB
