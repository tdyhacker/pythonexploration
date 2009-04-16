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
    Column("state", String(2)),
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

class Contact(object):
    def __init__(self, *args):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.nick_name = nick_name
        self.birthday = birthday
        self.street_address = street_address
        self.state = state
        self.country = country
        self.city = city
        self.zipcode = zipcode
        self.relationship_id = relationship_id

class Email(object):
    pass

class Type(object):
    pass

class Relationship(object):
    def __init__(self, group):
        self.group = group
    
    def __repr__(self):
        return "%s" % self.group


mapper(Contact, contacts_table, properties={'relationship':relation(Relationship, backref="people"),
                                            'emails':relation(Email, secondary=contact_email_xref_table, backref="person")})
mapper(Email, emails_table, properties={'groups':relation(Type, backref="people")})
mapper(Relationship, relationships_table)
mapper(Type, types_table)