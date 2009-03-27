import sqlalchemy as sa
from yinyang.model import meta

# Non-reflected tables may be defined and mapped at module level
login_table = sa.Table("logins", meta.metadata,
    sa.Column("id", sa.types.Integer, primary_key=True, nullable=False),
    sa.Column("name", sa.types.String(64), nullable=False),
    sa.Column("password", sa.types.String(64), nullable=False),
    )

class Login(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password
    
    def __repr__(self):
        return "<Login Name: %s Password: %s>" % (self.name, self.password)

#orm.mapper(Login, login_table) # Does this really have to be done in the __init__.py file?
