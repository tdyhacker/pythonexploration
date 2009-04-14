#!/usr/bin/env python
import sqlalchemy as sa
from sqlalchemy import orm
from datetime import datetime
from re import compile

from movies.model import meta

titles_table = sa.Table("Some table name", meta.metadata,
    sa.Column("id", sa.types.Integer, primary_key=True),
    sa.Column("column", sa.types.Text),
    sa.Column("column", sa.types.Date),
    sa.Column("column", sa.types.Integer),
    sa.Column("column", sa.types.String(5)),
    sa.Column("column", sa.types.Integer, sa.ForeignKey("categories.id"), nullable=False),
    )

class d_b(object):
    def __init__(self, **kws):
        ":D"
    
    def __repr__(self):
        return "Happy face"


title_actor_xref_table = sa.Table("title_actor_xref", meta.metadata,
    sa.Column("id", sa.types.Integer, primary_key=True),
    sa.Column("actor_id", sa.types.Integer, sa.ForeignKey("actors.id")),
    sa.Column("title_id", sa.types.Integer, sa.ForeignKey("titles.id")),
    sa.Column("character_name", sa.types.Text)
    )

class Character(object):
    def __init__(self, character_name):
        self.character_name = character_name
    
    def __repr__(self):
        return "<%s: %s>" % (self.__class__, self.character_name)


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

    def __repr__(self):
        return "<%s: %s, %s>" % (self.__class__, self.last_name, self.first_name)


orm.mapper(Title, titles_table, properties={'category':orm.relation(Category, backref="titles"),
                                            'characters':orm.relation(Character, backref="titles")})
orm.mapper(Actor, actors_table)
orm.mapper(Category, categories_table)
orm.mapper(Character, title_actor_xref_table, properties={"actor": orm.relation(Actor)})