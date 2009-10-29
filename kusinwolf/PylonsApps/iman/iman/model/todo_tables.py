#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Text, Integer, String, TIMESTAMP, Boolean, INT, DateTime, CHAR
from sqlalchemy.orm import mapper, relation
from datetime import datetime
from re import compile
from webhelpers.html import tags

# Any tables that do not need regeneration
from account_tables import User
from base_class import Attribute

from iman.model import meta

tasks_table = Table("task", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("task", Text),
    #Column("category", INT, ForeignKey("category.id")),
    #Column("priority", INT, ForeignKey("priority.id")),
    Column("user_id", INT, ForeignKey("users.uid")),
    Column("created", DateTime(), default = datetime.now),
    Column("modified", TIMESTAMP()),
    )

t_to_p_xref_table = Table("task_to_priority_xref", meta.metadata,
    Column("task_id", Integer, ForeignKey("task.id")),
    Column("priority_id", INT, ForeignKey("priority.id")),
    )

priorities_table = Table("priority", meta.metadata,
    Column("id", INT, primary_key=True),
    Column("severity", INT, unique=True),
    Column("name", Text),
    Column("color", CHAR(6)),
    Column("created", DateTime(), default = datetime.now),
    Column("modified", TIMESTAMP),
    )
# alter table priority add column color CHAR(6) default '000000';

t_to_c_xref_table = Table("task_to_category_xref", meta.metadata,
    Column("task_id", Integer, ForeignKey("task.id")),
    Column("category_id", INT, ForeignKey("category.id")),
    )

categories_table = Table("category", meta.metadata,
    Column("id", INT, primary_key=True),
    Column("name", Text),
    Column("color", CHAR(6)),
    Column("created", DateTime(), default = datetime.now),
    Column("modified", TIMESTAMP()),
    )
# alter table category add column color CHAR(6) default '000000';

class Task(Attribute):
    def __repr__(self):
        return "Task: %(task)s" % self.__dict__

class Category(Attribute):
    def __repr__(self):
        return "Category: %(name)s" % self.__dict__
    
    def _menu_repr_(self):
        return "%(name)s" % self.__dict__
    
class Priority(Attribute):
    def __repr__(self):
        return "Priority: %(name)s(%(severity)s)" % self.__dict__
    
    def _menu_repr_(self):
        return "%(name)s" % self.__dict__


mapper(Task, tasks_table, properties={'category' : relation(Category, secondary=t_to_c_xref_table, backref="tasks"),
                                      'priority' : relation(Priority, secondary=t_to_p_xref_table, backref="tasks"),
                                      'user' : relation(User, backref="tasks")})
mapper(Priority, priorities_table)
mapper(Category, categories_table)



