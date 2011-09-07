# -*- coding: UTF-8 -*-

# Database
DATABASE = 'blackboard/blackboard.sqlite3'
DBSCHEMA = 'blackboard/dbschema.sql'

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
