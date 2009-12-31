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
    Column("lastlogin", DateTime()),
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
    
    def hasNotViewedRecently(self, question):
        '''
            If the User has viewed the question before but not since the last post
        '''
        def findComparingView(user, question_id):
            for view in user.last_viewed: # Check all the viewed questions
                if view.question_id == question_id: # See if the Question is in the list
                    return view
            return None
        
        view = findComparingView(self, question.id) # this is the question that needs to be checked
        
        if view != None:
            for loc in range(1, len(question.responses) + 1): # Reverse order the list of 
                if question.responses[-1 * loc].modified >= view.last_viewed: # Does the last_viewing time beat the post time?
                    return True # A new response was added
                for comment in question.responses[-1 * loc].comments: # Check all comments
                    if comment.modified >= view.last_viewed: # Does the last_viewing time beat the post time?
                        return True # A new comment was added
            
        elif view == None:
            return True # Never viewed
        
        return False # No new comments or repsonses