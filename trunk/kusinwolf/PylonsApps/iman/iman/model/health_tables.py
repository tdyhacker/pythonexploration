#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Boolean, CHAR, DateTime, Float, INT, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import mapper, relation
from datetime import datetime

# Any tables that do not need regeneration
from base_class import Attribute

from webhelpers.html import tags
from iman.model import meta

weights_table = Table("weights", meta.metadata,
    Column("id", INT, primary_key=True),
    Column("weight", Float(precision = 7)),
    Column("units", Integer, ForeignKey("units.id")),
    Column("user_id", Integer, ForeignKey("users.uid")),
    Column("created", DateTime(), default = datetime.now),
    )

units_table = Table("units", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("unit", CHAR(16)),
    Column("digest", CHAR(6)),
    )

class Weight(Attribute):
    def __repr__(self):
        return "Weight: %(weight)s" % self.__dict__

class Unit(Attribute):
    def __repr__(self):
        return "Unit: %(unit)s Digest: %(digest)s" % self.__dict__
    
    def _menu_repr_(self):
        return "%(unit)s" % self.__dict__