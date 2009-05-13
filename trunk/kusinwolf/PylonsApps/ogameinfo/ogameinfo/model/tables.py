#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Text, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import mapper, relation
from datetime import datetime
from re import compile

from ogameinfo.model import meta

alliances_table = Table("alliances", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    Column("rank", Integer),
    Column("members", Integer),
    Column("points", Integer),
    Column("last_updated", TIMESTAMP(), default = datetime.now()),
    )

attacks_table = Table("attacks", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("planet_id", Integer, ForeignKey("planets.id")),
    Column("player_id", Integer, ForeignKey("players.id")),
    Column("attacked_at", TIMESTAMP(), default = datetime.now()),
    )

buildings_table = Table("buildings", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    )

defences_table = Table("defences", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    )

# Generated from Messages, uses all xref tables if info is provided
espionages_table = Table("espionages", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("counter_espionage", Integer),
    Column("created", TIMESTAMP()),
    )

e_p_xref_table = Table("espionages_planets_xref", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("planet_id", Integer, ForeignKey("planets.id")),
    Column("espionage_id", Integer, ForeignKey("espionages.id")),
    )

e_rs_xref_table = Table("espionages_resources_xref", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("resource_id", Integer, ForeignKey("resources.id")),
    Column("espionage_id", Integer, ForeignKey("espionages.id")),
    Column("amount", Integer),
    )

e_s_xref_table = Table("espionages_ships_xref", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("ship_id", Integer, ForeignKey("ships.id")),
    Column("espionage_id", Integer, ForeignKey("espionages.id")),
    Column("amount", Integer),
    )

e_d_xref_table = Table("espionages_defences_xref", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("defence_id", Integer, ForeignKey("defences.id")),
    Column("espionage_id", Integer, ForeignKey("espionages.id")),
    Column("amount", Integer),
    )

e_rh_xref_table = Table("espionages_researches_xref", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("resource_id", Integer, ForeignKey("researches.id")),
    Column("espionage_id", Integer, ForeignKey("espionages.id")),
    Column("level", Integer),
    )

e_b_xref_table = Table("espionages_buildings_xref", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("building_id", Integer, ForeignKey("buildings.id")),
    Column("espionage_id", Integer, ForeignKey("espionages.id")),
    Column("level", Integer),
    )

# Generated from viewing
players_table = Table("players", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    Column("rank", Integer),
    Column("alliance_id", Integer, ForeignKey("alliances.id"), default=0),
    Column("points", Integer),
    Column("last_updated", TIMESTAMP(), default = datetime.now()),
    )

players_planets_xref_table = Table("players_planets_xref", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("planet_id", Integer, ForeignKey("planets.id")),
    Column("player_id", Integer, ForeignKey("players.id")),
    )

players_espionages_xref_table = Table("players_espionages_xref", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("espionages_id", Integer, ForeignKey("espionages.id")),
    Column("player_id", Integer, ForeignKey("players.id")),
    )

# One player for many planets max 9
planets_table = Table("planets", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    Column("galaxy", Integer),
    Column("system", Integer),
    Column("orbit", Integer), # What planet number is it, 1 - 15
    Column("moon", Boolean),
    Column("last_updated", TIMESTAMP(), default = datetime.now()),
    )

resources_table = Table("resources", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    )

researches_table = Table("researches", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    )

ships_table = Table("ships", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text),
    )

users_table = Table("users", meta.metadata,
    Column("id", Integer, primary_key=True),
    Column("username", Text),
    Column("firstname", Text),
    Column("lastname", Text),
    Column("password", Text),
    Column("created", TIMESTAMP(), default = datetime.now()),
    )


class Building_type(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "Building Object"

class Defence_type(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "Defence Object"

class Ship_type(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "Ship Object"

class Research_type(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "Research Object"

class Resource_type(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "Resource Object"

class Building(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "Level %s, %s" % (self.level, self.type.name)

class Research(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "Level %s of %s" % (self.level, self.type.name)

class Resource(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "%sx %s" % (self.amount, self.type.name)

class Defence(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        if self.amount != 1:
            return "%sx %ss" % (self.amount, self.type.name)
        else:
            return "%sx %s" % (self.amount, self.type.name)

class Ship(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        if self.amount != 1:
            return "%sx %ss" % (self.amount, self.type.name)
        else:
            return "%sx %s" % (self.amount, self.type.name)

class Espionage(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "Espionage Report on %s at %d:%d:%d" % (self.owner[0].name, self.planet[0].galaxy, self.planet[0].system, self.planet[0].orbit)

class Attack(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "Attack Object"

class Alliance(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "Alliance Object"

class Planet(object):    
    def __init__(self, **kws):
        
        # Default values
        self.moon = False
        
        # Limits
        # Galaxy is from 1..9
        # System is from 1..500
        # Orbit is from 1..15
        
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "Planet Object"

class Player(object):
    def __init__(self, **kws):
        
        # Default values
        self.alliance_id = 1
        
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "Player Object"

class User(object):
    def __init__(self, **kws):
        for word in kws:
            self.__setattr__(word, kws[word])
    
    def __repr__(self):
        return "User Object"

mapper(Attack, attacks_table)
mapper(Resource_type, resources_table)
mapper(Research_type, researches_table)
mapper(Defence_type, defences_table)
mapper(Building_type, buildings_table)
mapper(Planet, planets_table)
mapper(User, users_table)
mapper(Ship_type, ships_table)
mapper(Alliance, alliances_table)

mapper(Building, e_b_xref_table, properties={'type':relation(Building_type)})
mapper(Research, e_rh_xref_table, properties={'type':relation(Research_type)})
mapper(Resource, e_rs_xref_table, properties={'type':relation(Resource_type)})
mapper(Defence, e_d_xref_table, properties={'type':relation(Defence_type)})
mapper(Ship, e_s_xref_table, properties={'type':relation(Ship_type)})

mapper(Player, players_table, properties={'alliance':relation(Alliance, backref="players"),
                                          'planets':relation(Planet, secondary=players_planets_xref_table, backref="player"),
                                          'attacked':relation(Attack, backref="attackers"),
                                          'espionaged':relation(Espionage, secondary=players_espionages_xref_table, backref="owner")
                                          })

mapper(Espionage, espionages_table, properties={'resources':relation(Resource),
                                                'fleet':relation(Ship),
                                                'defences':relation(Defence),
                                                'buildings':relation(Building),
                                                'research':relation(Research),
                                                'planet':relation(Planet, secondary=e_p_xref_table, backref="espionage_reports"),
                                                })


