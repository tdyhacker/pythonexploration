#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Text, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import mapper, relation
from datetime import datetime
from re import compile
from webhelpers.html import tags

from iman.model import meta

questions_table = Table("questions", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("question", Text),
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
    Column("created", TIMESTAMP(), default = datetime.now()),
    Column("modified", TIMESTAMP(), default = datetime.now()),
    )

class Question(object):
    def __init__(self, **kws):
        for attr in kws:
            self.__setattr__(attr, kws[attr])
    
    def __repr__(self):
        return "Question: %s" % self.question

class Response(object):
    def __init__(self, **kws):
        for attr in kws:
            self.__setattr__(attr, kws[attr])
    
    def __repr__(self):
        return "Response: %s" % self.question

mapper(Question, questions_table)
mapper(Response, responses_table, properties={'question':relation(Question, secondary=_xref_table, backref="responses")})



