#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Text, Integer, String, Boolean, INT, DateTime, TIMESTAMP
from sqlalchemy.orm import mapper, relation
from datetime import datetime
from re import compile
from webhelpers.html import tags

# Any tables that do not need regeneration
from base_class import Attribute

from iman.model import meta

ips_table = Table("ips", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("ip", String(128)),
    Column("until", DateTime()),
    Column("created", DateTime(), default=datetime.now),
    Column("modified", TIMESTAMP()), # automatically updated with any changes through the ORM
    )

class IP(Attribute):
    def __repr__(self):
        return "IP: %(ip)s banned until %(until)s" % self.__dict__

mapper(IP, ips_table)



