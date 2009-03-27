import sqlalchemy as sa
from sqlalchemy import orm
from datetime import datetime
from re import compile

from movies.model import meta

titles_table = sa.Table("titles", meta.metadata,
    sa.Column("id", sa.types.Integer, primary_key=True),
    sa.Column("name", sa.types.Text),
    sa.Column("release_date", sa.types.Date),
    sa.Column("duration", sa.types.Integer),
    sa.Column("rating", sa.types.String(5)),
    sa.Column("category_id", sa.types.Integer, sa.ForeignKey("categories.id"), nullable=False),
    )

class Title(object):
    def __init__(self, **kws):
        #if type(kws['release_date']) != datetime:
            #newdate = compile("(\d{2})[-\s.~_|/\/](\d{2})[-\s.~_|/\/](\d{4})").match(kws['release_date']).groups()
            #kws['release_date'] = datetime(month=int(newdate[0]), day=int(newdate[1]), year=int(newdate[2]))
        kws['release_date'] = datetime(month=int(kws['month']), day=int(kws['day']), year=int(kws['year']))
        if type(kws['duration']) != int:
            kws['duration'] = int(kws['duration'])
        self.name = kws['name']
        self.release_date = kws['release_date']
        self.duration = kws['duration']
        self.rating = kws['rating']
        self.category_id = kws['categories']
    
    def __repr__(self):
        return "<%s: %s, %s, %s, %s>" % (self.__class__, self.name, self.release_date, self.release_date, self.category_id)
