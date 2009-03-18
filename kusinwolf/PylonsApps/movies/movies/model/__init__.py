"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from movies.model import meta

from titles import Title, titles_table
from actors import Actor, actors_table
from categories import Category, categories_table
from title_actor_xref import title_actor_xref_table, Character

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=engine)
    meta.engine = engine

orm.mapper(Title, titles_table, properties={'category':orm.relation(Category, backref="titles"),
                                            'characters':orm.relation(Character, backref="titles")})
orm.mapper(Actor, actors_table)
orm.mapper(Category, categories_table)
orm.mapper(Character, title_actor_xref_table, properties={"actor": orm.relation(Actor)})


## Non-reflected tables may be defined and mapped at module level
#foo_table = sa.Table("Foo", meta.metadata,
#    sa.Column("id", sa.types.Integer, primary_key=True),
#    sa.Column("bar", sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass
