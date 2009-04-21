#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Text, Integer, String, Date
from sqlalchemy.orm import mapper, relation
from datetime import datetime
from re import compile

from univaddbook.model import meta

contacts_table = Table("contacts", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", Text),
    Column("middle_name", Text),
    Column("last_name", Text),
    Column("nick_name", Text),
    Column("birthday", Date),
    Column("street_address", Text),
    Column("State", Integer, ForeignKey("states.id")),
    Column("country", Text),
    Column("city", Text),
    Column("zipcode", Integer),
    Column("relationship_id", Integer, ForeignKey("relationships.id")),
    )

contact_email_xref_table = Table("contact_email_xref", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("contact_id", Integer, ForeignKey("contacts.id")),
    Column("email_id", Integer, ForeignKey("emails.id")),
    )

emails_table = Table("emails", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("email", Text),
    Column("type_id", Integer, ForeignKey("types.id"), nullable=False),
    )

types_table = Table("types", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    )
# Perfessional
# Personal
# Other

relationships_table = Table("relationships", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("group", Text),
    )
# Family
# Friends
# Co-workers
# Other

states_table = Table("states", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("state", Text),
    Column("short", String(2)),
    )

class Contact(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Email(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "%s, %s" % (self.email, self.group)

class Type(object):
    def __repr__(self):
        return "%s" % self.name

class Relationship(object):
    def __init__(self, group):
        self.group = group
    
    def __repr__(self):
        return "%s" % self.group

class State(object):
    pass

mapper(Contact, contacts_table, properties={'relationship':relation(Relationship, backref="contacts"),
                                            'emails':relation(Email, secondary=contact_email_xref_table, backref="contact"),
                                            'state':relation(State, backref="contacts")})
mapper(Email, emails_table, properties={'group':relation(Type, backref="emails")})
mapper(Relationship, relationships_table)
mapper(Type, types_table)
mapper(State, states_table)
