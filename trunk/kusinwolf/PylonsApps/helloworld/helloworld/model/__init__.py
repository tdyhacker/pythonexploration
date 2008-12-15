import datetime
from time import strftime
from sqlalchemy import create_engine, Table, Column, MetaData, ForeignKey, and_, or_, ForeignKey
from sqlalchemy.types import DateTime, String, Integer, Boolean
from sqlalchemy.orm import mapper, sessionmaker, clear_mappers, relation, scoped_session

from helloworld.model import meta

# All of the tables
from helloworld.model import link_table

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""

    sm = sessionmaker(autoflush=True, transactional=True, bind=engine)

    meta.engine = engine
    meta.Session = scoped_session(sm)
    

