#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Boolean, CHAR, DateTime, INT, Integer, Float, String, Text, TIMESTAMP
from sqlalchemy.orm import mapper, relation
from datetime import datetime
from re import compile
from crypt import crypt

# Any tables that do not need regeneration
from base_class import Attribute

from webhelpers.html import tags
from eve_data.model import meta

invtypes_table = Table("invTypes", meta.metadata,
    Column("typeID", Integer, primary_key=True),
    Column("groupID", Integer),
    Column("typeName", CHAR(100)),
    Column("description", CHAR(3000)),
    Column("graphicID", Integer),
    Column("radius", Float),
    Column("mass", Float),
    Column("volume", Float),
    Column("capacity", Float),
    Column("portionSize", Integer),
    Column("raceID", Integer),
    Column("basePrice", Float),
    Column("published", Integer),
    Column("marketGroupID", Integer),
    Column("chanceofDuplicating", Float),
    )

class invType(Attribute):
    def __repr__(self):
        return "invType: %(typeID)s" % self.__dict__



