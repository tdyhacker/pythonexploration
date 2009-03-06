import sqlalchemy as sa
from sqlalchemy import orm
from datetime import datetime
from re import compile

from movies.model import meta

categories_table = sa.Table("categories", meta.metadata,
    sa.Column("id", sa.types.Integer, primary_key=True),
    sa.Column("name", sa.types.Text)
    )

class Category(object):
    def __init__(self, **kws):
        self.name = kws['name']
