import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import types

def init_model(bind):
    """Call me at the beginning of the application.
       'bind' is a SQLAlchemy engine or connection, as returned by
       sa.create_engine, sa.engine_from_config, or engine.connect().
    """
    global engine, Session
    engine = bind
    Session = orm.scoped_session(
        orm.sessionmaker(transactional=True, autoflush=True, bind=bind))
    orm.mapper(Blog, blog_table,
        order_by=[blog_table.c.date.desc()])

meta = sa.MetaData()

blog_table = sa.Table("Blog", meta,
    sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
    sa.Column("subject", types.String(255)),
    sa.Column("author", types.String(255)),
    sa.Column("date", types.DateTime()),
    sa.Column("content", types.Text()), #or types.TEXT() - to .Text() doesn't exists :/ 
    )

class Blog(object):
    def __str(self):
        return self.title

