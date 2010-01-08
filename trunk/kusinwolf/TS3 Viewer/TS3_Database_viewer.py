import sqlalchemy
import sqlite3

# Database name
database = "ts3server.sqlitedb"

# Database engine
engine = sqlalchemy.create_engine('sqlite:///%s' % database, module=sqlite3.dbapi2)

# query used
query = "select * from group_channel_to_client"

# query object
query_object = engine.text(query).execute()

for key in query_object.keys:
    print "%s\t" % key,
print ''

for row in query_object.fetchall():
    for item in row:
        print "%s\t" % item,
    print ''