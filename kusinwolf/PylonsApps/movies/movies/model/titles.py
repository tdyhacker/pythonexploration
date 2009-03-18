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
        if type(kws['release_date']) != datetime:
            newdate = compile("(\d{4})[-\s.~_|/\\]([0-1][0-9])[-\s.~_|/\\]([0-3][0-9])").match(kws['release_date'])
            kws['release_date'] = datetime(newdate[0], newdate[1], newdate[2])
        if type(kws['duration']) != int:
            kws['duration'] = int(kws['duration'])
        self.name = kws['name']
        self.release_date = kws['release_date']
        self.duration = kws['duration']
        self.rating = kws['rating']
        self.categories = kws['categories']
    
    def __repr__(self):
        return "<%s: %s, %s>" % (self.__class__, self.name, self.release_date)
