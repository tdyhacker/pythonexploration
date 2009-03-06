import sqlalchemy as sa
from sqlalchemy import orm
from datetime import datetime
from re import compile

from movies.model import meta

actors_table = sa.Table("actors", meta.metadata,
    sa.Column("id", sa.types.Integer, primary_key=True),
    sa.Column("first_name", sa.types.Text),
    sa.Column("last_name", sa.types.Text)
    )

class Actor(object):
    def __init__(self, **kws):
        self.first_name = kws['first_name']
        self.last_name = kws['last_name']
        self.birthday = kws['birthday']
