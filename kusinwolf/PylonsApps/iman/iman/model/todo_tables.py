#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Text, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import mapper, relation
from datetime import datetime
from re import compile
from webhelpers.html import tags

# Any tables that do not need regeneration
from tables import User, Attribute

from iman.model import meta

tasks_table = Table("task", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("", Text),
    Column("category", Integer, ForeignKey("category.id")),
    Column("priority", Integer, ForeignKey("priority.id")),
    Column("user_id", Integer, ForeignKey("users.uid")),
    Column("created", TIMESTAMP(), default = datetime.now()),
    Column("modified", TIMESTAMP(), default = datetime.now()),
    )

t_to_p_xref_table = Table("task_to_priority_xref", meta.metadata,
    Column("question_id", Integer, ForeignKey("questions.id")),
    Column("response_id", Integer, ForeignKey("responses.id")),
    )

prioritys_table = Table("priority", meta.metadata,
    Column("severity", Integer, unique=True),
    Column("name", Text),
    Column("created", TIMESTAMP(), default = datetime.now()),
    Column("modified", TIMESTAMP(), default = datetime.now()),
    )

categories_table = Table("category", meta.metadata,
    Column("id", Integer, unique=True, autoincrement=True),
    Column("name", Text),
    Column("created", TIMESTAMP(), default = datetime.now()),
    Column("modified", TIMESTAMP(), default = datetime.now()),
    )


class Question(object, Attribute):
    def __repr__(self):
        return "Question: %s" % self.question

class Response(object, Attribute):
    def __repr__(self):
        return "Response: %s" % self.question


mapper(Question, questions_table, properties={'user' : relation(User, backref="questions")})
mapper(Response, responses_table, properties={'question' : relation(Question, secondary=r_to_q_xref_table, backref="responses"),
                                              'user' : relation(User, backref="responses")})



