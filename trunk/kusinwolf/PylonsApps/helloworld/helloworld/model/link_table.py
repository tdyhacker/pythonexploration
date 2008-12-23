from time import strftime
from re import compile

from sqlalchemy import create_engine, Table, Column, MetaData, ForeignKey, and_, or_, ForeignKey
from sqlalchemy.types import DateTime, String, Integer, Boolean, Text
from sqlalchemy.orm import mapper, sessionmaker, clear_mappers, relation, scoped_session

from helloworld.model.meta import *

from helloworld.model.tags_table import *

#links_table = Table("Saved_links_old", meta.metadata,
#                        Column("id", Integer, primary_key=True),
#                        Column("notes", String(512)), # text
#                        Column("link", String(512)), # text
#                        Column("tags", String(128)), # text
#                        Column("addtime", String(32)), # datetime
#                        Column("inatime", String(32)), # datetime
#                        Column("modtime", String(32)), # datetime
#                        Column("active", Boolean()))

links_table = Table("Saved_links", metadata,
                        Column("id", Integer, primary_key=True),
                        Column("notes", Text), # text
                        Column("link", Text), # text
                        Column("addtime", Text), # datetime
                        Column("inatime", Text), # datetime
                        Column("modtime", Text), # datetime
                        Column("active", Boolean()))

class Links(object):
    def __init__(self, link, notes=None, active=True):
        self.link = None        # Name
        self.setLink(link)
        self.notes = None      # Notes
        self.setNotes(notes)
        self.tags = None        # Tags
        self.setTags(tags)
        # Contains the time it was added, it is not a passable value, time should be absolut
        #self.addtime = datetime.datetime.now()
        self.addtime = strftime("%b %d %Y - %H:%M:%S")
        if active:
            self.inatime = "Still Active"
        else:
            self.inatime = strftime("%b %d %Y - %H:%M:%S")
        self.modtime = self.addtime
        self.active = active
        
    def __repr__(self):
        return ("<Link('%s', '%s','%s', '%s', '%s', Active: '%s', Inactivated: '%s', Modifed: '%s')>"
            % (self.id, self.link, self.notes, self.tags, self.addtime, self.active, self.inatime, self.modtime))
    
    def __cmp__(self, right):
        return self.link == right.link
    
    def __str__(self):
        return "Link: %s\nNotes: %s\nTags: %s\nActive: %s\t[Added: %s\t\t[Modifed: %s\t\t[Inactivated: %s" % (self.link, self.notes, self.tags, self.active, self.addtime, self.modtime, self.inatime)
    
    def getID(self):
        return self.id
    
    def setLink(self, name = None):
        edited = False
        
        if self.link != name and name != None:
            if not compile("http://(.*)").match(name):
                name = "http://%s" % str(name)
            if not compile("(.*).com(.*)").match(name):
                name = "%s.com" % str(name)
            self.link = str(name)
            edited = True
        
        return edited

    def getLink(self):
        return self.link
    
    def setNotes(self, notes = None):
        edited = False
        
        if self.notes != notes and notes != None:
            self.notes = str(notes)
            edited = True
        
        return edited
    
    def getNotes(self):
        return self.notes
    
    def setTags(self, tags = None):
        edited = False
        
        if self.tags != tags and tags != None:
            self.tags = str(tags).lower()
            edited = True
        
        return edited
    
    def getTags(self):
        return "oops"
    
    def parseTags(self):
        return compile('(\S\w*)').findall(self.tags)
    
    def setActivity(self, act):
        edited = False
        
        if act == "True":
            act = True
        elif act == "False":
            act = False
        else:
            print "Wrong arguments, boolean or string equivalent comparisons"
            return False
            
        if self.active != act:
                self.active = act
                edited = True
        
        return edited
    
    def getActivity(self):
        return self.active
    
    def setModTime(self):
        self.modtime = strftime("%b %d %Y - %H:%M:%S")
    
    def getModTime(self):
        return self.modtime
    
    def setAddTime(self):
        self.addtime = strftime("%b %d %Y - %H:%M:%S")
    
    def getAddTime(self):
        return self.addtime
    
    def setInaTime(self):
        self.inatime = strftime("%b %d %Y - %H:%M:%S")
    
    def getInaTime(self):
        return self.inatime
    
mapper(Links, links_table)