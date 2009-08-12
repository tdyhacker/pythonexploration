#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Text, Integer, String, TIMESTAMP, Boolean, INT, DateTime
from sqlalchemy.orm import mapper, relation
from datetime import datetime
from re import compile
from crypt import crypt

# Any tables that do not need regeneration
from base_class import Attribute

from webhelpers.html import tags
from iman.model import meta

users_table = Table("users", meta.metadata,
    Column("uid", INT, primary_key=True),
    Column("username", Text),
    Column("firstname", Text),
    Column("lastname", Text),
    Column("password", Text),
    Column("pass_key", String(2)),
    Column("group_uid", INT),
    Column("created", DateTime(), default = datetime.now),
    Column("modified", TIMESTAMP()),
    )

class User(Attribute):
    def __repr__(self):
        return "User: %(firstname)s '%(username)s' %(lastname)s" % self.__dict__
    
    def getByID(self, id):
        return meta.Session.query(User).filter_by(uid=id).first()
    
    def isUnique(self, username):
        return meta.Session.query(User).filter_by(username=username.lower()).first() is None
    
    def authenticate(self, username, password):
        ''' Authenticates the username and password with the database '''
        user = meta.Session.query(User).filter_by(username=username).first()
        if user and user.password == crypt(password, user.pass_key):
            return user
        else:
            return None
    
    def validatePassword(self, password):
        print self.password, "'%s'" % password, crypt(str(password), str(self.created.second)), self.created.second
        if str(self.password) == crypt(str(password), str(self.pass_key)):
            return True
        else:
            return False
    
    def changePassword(self, new_password):
        self.password = crypt(new_password, str(self.pass_key))
        
mapper(User, users_table)