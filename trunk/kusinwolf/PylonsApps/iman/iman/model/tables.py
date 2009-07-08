#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Text, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import mapper, relation
from datetime import datetime
from re import compile
from webhelpers.html import tags

from iman.model import meta

users_table = Table("users", meta.metadata,
    Column("uid", Integer, primary_key=True),
    Column("username", Text),
    Column("firstname", Text),
    Column("lastname", Text),
    Column("password", Text),
    Column("group_uid", Integer),
    Column("created", TIMESTAMP(), default = datetime.now()),
    )

questions_table = Table("questions", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("question", Text),
    Column("user_id", Integer, ForeignKey("users.uid")),
    Column("created", TIMESTAMP(), default = datetime.now()),
    Column("modified", TIMESTAMP(), default = datetime.now()),
    )

r_to_q_xref_table = Table("responses_to_question_xref", meta.metadata,
    Column("question_id", Integer, ForeignKey("questions.id")),
    Column("response_id", Integer, ForeignKey("responses.id")),
    )

responses_table = Table("responses", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("response", Text),
    Column("user_id", Integer, ForeignKey("users.uid")),
    Column("created", TIMESTAMP(), default = datetime.now()),
    Column("modified", TIMESTAMP(), default = datetime.now()),
    )

class Question(object):
    def __init__(self, **kws):
        for attr in kws:
            self.__setattr__(attr, kws[attr])
    
    def __repr__(self):
        return "Question: %(question)s" % self.__dict__

class Response(object):
    def __init__(self, **kws):
        for attr in kws:
            self.__setattr__(attr, kws[attr])
    
    def __repr__(self):
        return "Response to %(question)s" % self.__dict__

class User(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
        
        # Assign work around values
        self.id = self.__dict__.get("uid")
    
    def __repr__(self):
        return "User: %(firstname)s '%(username)s' %(lastname)s" % self.__dict__
    
mapper(User, users_table)
mapper(Question, questions_table, properties={'user' : relation(User, backref="questions")})
mapper(Response, responses_table, properties={'question' : relation(Question, secondary=r_to_q_xref_table, backref="responses"),
                                              'user' : relation(User, backref="responses")})



