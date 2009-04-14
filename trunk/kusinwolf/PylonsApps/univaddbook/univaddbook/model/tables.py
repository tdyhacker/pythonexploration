#!/usr/bin/env python
from sqlalchemy import Column, Table
from sqlalchemy.types import Text, Integer, String
from sqlalchemy.orm import mapper, relation
from datetime import datetime
from re import compile

from movies.model import meta

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
    Column("contact_id", Integer, ForeignKey("contact.id")),
    Column("email_id", Integer, ForeignKey("email.id")),
    )

emails_table = Table("emails", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("email", Text),
    Column("type_id", Integer, ForeignKey("id"), nullable=False),
    )

types_table = Table("types", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    )

relationships_table = Table("relationships", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("group", Text),
    )

class Contact(object):
    pass
class Email(object):
    pass
class Type(object):
    pass
class Relationship(object):
    pass


mapper(Contact, contacts_table, properties={'relationship':relation(Relationship, backref="people"),
                                                'emails':relation(Email, secondary=contact_email_xref_table, backref="person")})
mapper(Email, emails_table)
mapper(Relationship, relationships_table)
mapper(Type, types_table)