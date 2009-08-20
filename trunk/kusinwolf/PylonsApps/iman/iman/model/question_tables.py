#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Text, Integer, String, TIMESTAMP, Boolean, INT, DateTime
from sqlalchemy.orm import mapper, relation
from datetime import datetime
from re import compile
from crypt import crypt

# Any tables that do not need regeneration
from base_class import Attribute
from account_tables import User

from webhelpers.html import tags
from iman.model import meta


questions_table = Table("questions", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("question", Text),
    Column("user_id", INT, ForeignKey("users.uid")),
    Column("created", DateTime(), default = datetime.now),
    Column("modified", TIMESTAMP()),
    )

r_to_q_xref_table = Table("responses_to_question_xref", meta.metadata,
    Column("question_id", Integer, ForeignKey("questions.id")),
    Column("response_id", Integer, ForeignKey("responses.id")),
    )

responses_table = Table("responses", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("response", Text),
    Column("user_id", INT, ForeignKey("users.uid")),
    Column("created", DateTime(), default = datetime.now),
    Column("modified", TIMESTAMP()),
    )

class Question(Attribute):
    def __repr__(self):
        return "Question: %(question)s" % self.__dict__

class Response(Attribute):
    def __repr__(self):
        return "Response" % self.__dict__

mapper(Question, questions_table, properties={'user' : relation(User, backref="questions")})
mapper(Response, responses_table, properties={'question' : relation(Question, secondary=r_to_q_xref_table, backref="responses"),
                                              'user' : relation(User, backref="responses")})



