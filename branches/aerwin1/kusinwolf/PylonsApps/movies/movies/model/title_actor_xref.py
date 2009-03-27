import sqlalchemy as sa
from sqlalchemy import orm
from datetime import datetime
from re import compile

from movies.model import meta

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