#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Boolean, CHAR, DateTime, Float, INT, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import mapper, relation
from datetime import datetime

# Any tables that do not need regeneration
from base_class import Attribute

from webhelpers.html import tags
from iman.model import meta

events_table = Table("events", meta.metadata,
    Column("id", INT, primary_key=True),
    Column("start", DateTime()),
    Column("end", DateTime()),
    Column("title", Text),
    Column("description", Text),
    Column("image", Text),
    Column("link", Text),
    Column("isDuration", Boolean),
    Column("icon", Text),
    Column("caption", Text),
    Column("color", Text),
    Column("textColor", Text),
    Column("added", DateTime(), default = datetime.now),
    )

class Event(Attribute):
    def __repr__(self):
        return "Event: %(title)s" % self.__dict__
    
    def _menu_repr_(self):
        return "%(title)s" % self.__dict__
    
    #'start': '2009-12-24T00:00:00',
    #'end': '2011',
    #'title': 'Landschaft bei Montreuil',
    #'description': 'by Albert Gleizes, French Painter, 1881-1953',
    #'image': 'http://images.allposters.com/images/mer/1336_b.jpg',
    #'link': 'http://www.allposters.com/-sp/Landschaft-bei-Montreuil-Posters_i339007_.htm',
    #'isDuration' : true, // if the event needs a barred line
    #'icon' : "../dark-red-circle.png",
    #'caption' : ":D",
    #'color' : 'red',
    #'textColor' : 'green'