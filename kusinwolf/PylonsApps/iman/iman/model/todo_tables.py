#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Text, INTEGER, String, TIMESTAMP, Boolean
from sqlalchemy.orm import mapper, relation
from datetime import datetime
from re import compile
from webhelpers.html import tags

# Any tables that do not need regeneration
from tables import User, Attribute

from iman.model import meta

tasks_table = Table("task", meta.metadata,
    Column("id", INTEGER, primary_key=True),
    Column("task", Text),
    #Column("category", INTEGER, ForeignKey("category.id")),
    #Column("priority", INTEGER, ForeignKey("priority.id")),
    Column("user_id", INTEGER, ForeignKey("users.uid")),
    Column("created", TIMESTAMP(), default = datetime.now()),
    Column("modified", TIMESTAMP(), default = datetime.now()),
    )

t_to_p_xref_table = Table("task_to_priority_xref", meta.metadata,
    Column("task_id", INTEGER, ForeignKey("task.id")),
    Column("priority_id", INTEGER, ForeignKey("priority.id")),
    )

priorities_table = Table("priority", meta.metadata,
    Column("id", INTEGER, primary_key=True),
    Column("severity", INTEGER, unique=True),
    Column("name", Text),
    Column("created", TIMESTAMP(), default = datetime.now()),
    Column("modified", TIMESTAMP(), default = datetime.now()),
    )

t_to_c_xref_table = Table("task_to_category_xref", meta.metadata,
    Column("task_id", INTEGER, ForeignKey("task.id")),
    Column("category_id", INTEGER, ForeignKey("category.id")),
    )

categories_table = Table("category", meta.metadata,
    Column("id", INTEGER, primary_key=True),
    Column("name", Text),
    Column("created", TIMESTAMP(), default = datetime.now()),
    Column("modified", TIMESTAMP(), default = datetime.now()),
    )

class Task(Attribute):
    def __repr__(self):
        return "Task: %(task)s" % self.__dict__

class Category(Attribute):
    def __repr__(self):
        return "Category: %(name)s" % self.__dict__
    
class Priority(Attribute):
    def __repr__(self):
        return "Priority: %(name)s\(%(severity)s\)" % self.__dict__


mapper(Task, tasks_table, properties={'category' : relation(Category, secondary=t_to_c_xref_table, backref="tasks"),
                                      'priority' : relation(Priority, secondary=t_to_p_xref_table, backref="tasks"),
                                      'user' : relation(User, backref="tasks")})
mapper(Priority, priorities_table)
mapper(Category, categories_table)



