#!/usr/bin/env python
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Boolean, CHAR, DateTime, Float, INT, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import mapper, relation
from datetime import datetime

# Any tables that do not need regeneration
from base_class import Attribute

from webhelpers.html import tags
from iman.model import meta

events_table = Table("events", meta.metadata,
    Column("id", INT, primary_key=True),
    Column("start", DateTime(), default = "0000-00-00 00:00:00"), # Start date (Conversion is "YYYY-MM-DDTHH:MM:SS" on a 24 hour clock)
    Column("end", DateTime(), default = "0000-00-00 00:00:00"), # End date (Conversion is "YYYY-MM-DDTHH:MM:SS" on a 24 hour clock)
    Column("title", CHAR(64)), # Title shown in details and overview
    Column("description", Text), # Description displayed in details
    Column("image", Text), # Image displayed in details
    Column("link", Text), # Title Link to where ever they want to go
    Column("isDuration", Boolean, default = False), # If True then a barred line with the specified color is drawn
    Column("icon", CHAR(128)), # Selected icon name
    Column("caption", Text), # Popup text displayed on hover
    Column("color", CHAR(6)), # Color of the band
    Column("textColor", CHAR(6)), # Color of the title text
    Column("added", DateTime(), default = datetime.now),
    )

class Event(Attribute):
    def __repr__(self):
        return "Event: %(title)s" % self.__dict__
    
    def _menu_repr_(self):
        return "%(title)s" % self.__dict__
    
    def js_repr(self):
        '''This method is used to print out all required data for the JavaScript file read in by the timeline page'''
        
        p_dict = {}
        for group in ["title", "description", "image", "link", "isDuration", "icon", "caption", "color", "textColor"]:
            if (self.__dict__[group] != None) and (self.__dict__[group] != ''):
                p_dict[group] = str(self.__dict__[group]) # Fix all unicode notifications and stringless objects all at once
        print p_dict
        
        # Convert to a useable format
        if self.__dict__.get("start", None):
            p_dict["start"] = self.__dict__["start"] - timedelta(hours=6)
            p_dict["start"] = p_dict["start"].strftime("%Y-%m-%dT%H:%M:%S")
        
        # Convert to a useable format
        if self.__dict__.get("end", None) and self.__dict__.get("end") != "0000-00-00 00:00:00":
            p_dict["end"] = self.__dict__["end"] - timedelta(hours=6)
            p_dict["end"] = p_dict["end"].strftime("%Y-%m-%dT%H:%M:%S")
        
        return str("%s,\n" % p_dict)
    
    #'start': '2009-12-24T00:00:00',
    #'end': '2011',
    #'title': 'Landschaft bei Montreuil',
    #'description': 'by Albert Gleizes, French Painter, 1881-1953',
    #'image': 'http://images.allposters.com/images/mer/1336_b.jpg',
    #'link': 'http://www.allposters.com/-sp/Landschaft-bei-Montreuil-Posters_i339007_.htm',
    #'isDuration' : true, // if the event needs a barred line
    #'icon' : "../dark-red-circle.png",
    #'caption' : ":D",
    #'color' : 'red',
    #'textColor' : 'green'