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


questions_table = Table("questions", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("question", Text),
    Column("user_id", INT, ForeignKey("users.uid")),
    Column("public", Boolean, default = False),
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

u_v_of_q_xref_table = Table("user_views_of_question_xref", meta.metadata,
    Column("question_id", Integer, ForeignKey("questions.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.uid"), primary_key=True),
    Column("last_viewed", DateTime(), default = datetime.now),
    )

comments_table = Table("comments", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("comment", Text),
    Column("user_id", INT, ForeignKey("users.uid")),
    Column("created", DateTime(), default = datetime.now),
    Column("modified", TIMESTAMP()),
    )

c_to_r_xref_table = Table("comments_to_response_xref", meta.metadata,
    Column("comment_id", Integer, ForeignKey("comments.id")),
    Column("response_id", Integer, ForeignKey("responses.id")),
    )

class Question(Attribute):
    def __repr__(self):
        return "Question: %(question)s" % self.__dict__

class Response(Attribute):
    def __repr__(self):
        return "Response" % self.__dict__

class View(Attribute):
    def __repr__(self):
        return "last viewed %(last_viewed)s" % self.__dict__

class Comment(Attribute):
    def __repr__(self):
        return "Comment" % self.__dict__



