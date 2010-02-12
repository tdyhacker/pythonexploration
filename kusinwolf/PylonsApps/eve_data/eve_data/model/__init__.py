"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy.orm import mapper, relation

from eve_data.model import meta
from eve_data.model.invTypes import invtypes_table, invType

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

# =======================================================================================================
# By doing all of the mapping here, this prevents the python files from importing each other and breaking
# =======================================================================================================
# invTypes tables
# =======================================================================================================
mapper(invType, invtypes_table)
