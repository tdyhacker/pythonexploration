from time import strftime
from re import compile

from sqlalchemy import create_engine, Table, Column, MetaData, ForeignKey, and_, or_, sql
from sqlalchemy.types import DateTime, String, Integer, Boolean, Text
from sqlalchemy.orm import mapper, sessionmaker, clear_mappers, relation, scoped_session

from helloworld.model.meta import *

tag_table = Table("tag", metadata,
                        Column("id", Integer, primary_key=True),
                        Column("tag", Text))

link_xref_tag_table = Table("link_xref_tag", metadata,
                        Column("id", Integer, primary_key=True),
                        Column("link_id", Integer),
                        Column("tag_id", Integer, ForeignKey("tag.id")))

class Tag(object):
    def __init__(self, tag):
        self.inTable = False
        self.inTableID = -1
        
        self.tag = tag.lower()
        
        self.findDuplicate()
    
    def __repr__(self):
        return ("<Tag(ID: '%s' Name: '%s')>"
            % (self.id, self.tag))
    
    def findDuplicate(self):
        '''If the tag was found in the table already, then provide ID to be used instead of inserting'''
        found = Session.query(Tag).filter_by(tag=self.tag).all()
        if found:
            self.inTable = True
            self.inTableID = found[0].id
    
    def getName(self):
        return str(self.tag)

class Link_xref_tag(object):
    def __init__(self, link_id, tag_id):
        self.inTable = False
        self.link_id = link_id
        self.tag_id = tag_id
        
        self.findDuplicate()
    
    def __repr__(self):
        return ("<Tag(Xref Link ID: '%s' Xref Tag ID: '%s')>"
            % (self.link_id, self.tag_id))
    
    def findDuplicate(self):
        '''If the xref was found in the table already, then prevent a duplicate'''
        found = Session.query(Link_xref_tag).filter_by(link_id=self.link_id, tag_id=self.tag_id).all()
        if found:
            self.inTable = True

mapper(Tag, tag_table)
mapper(Link_xref_tag, link_xref_tag_table)