#!/usr/bin/env python
from datetime import datetime
from re import compile
from crypt import crypt

class Attribute(object):
    """Default class for all and any type of attribute for any object in an xml definition"""
    def __init__(self, **kws):
        for word in kws:
            self.addAttribute(word, kws[word], is_object=(type(kws[word]) not in [int, str, bool]))
            
        self._parent_ = self.__class__
    
    def addAttribute(self, name, value, is_object=False):
        """ is_object = False will convert any value input a string\n\n
            If you want to add anything to a list use appendToAttribute\n
            which will also check to see if the attribute exisits or not, great for being lazy\n
        """
        if not is_object and type(value) != bool:
            value = str(value).strip()
            
            if value.isdigit():
                value = int(value)
        
        self.__setattr__(str(name), value)
    
    def appendToAttribute(self, name, value, is_object=True, is_string=False):
        """ is_string is used to concatenate incoming strings together on an attribute\n
            This method adds an attribute as a list or appends to an existing list attribute
        """
        # if the value doesn't already exist, then make it
        if name not in self.__dict__:
            if not is_string:
                value = [value,]
            self.addAttribute(name, value, is_object=True)
        else:
            if is_string:
                self.__dict__[name] += value
            else:
                self.__dict__[name].append(value)
    
    def doesAttributeHaveValue(self, attribute, value, cls_validator = None):
        does = False
        
        if attribute in self.__dict__.keys():
            if type(self.__dict__[attribute]) == list or type(self.__dict__[attribute]) == tuple:
                for item in self.__dict__[attribute]:
                    if cls_validator == None and item == value:
                        does = True
                    elif cls_validator(item, value):
                        does = True
            elif cls_validator == None and self.__dict__[attribute] == value:
                does = True
            elif cls_validator(item, value):
                does = True
        
        return does
    
    def getSimilarAttributeWithValue(self, attribute, value, cls_validator = None):
        """ this method should only be called on known list attributes """
        if attribute in self.__dict__.keys():
            for item in self.__dict__[attribute]:
                if cls_validator == None and item == value:
                    return item
                elif cls_validator(item, value):
                    return item
        
        return None
    
    def getCopyWithout(self, remove = None):
        """ returns a dictionary copy of self without any of the attributes designated """
        rdic = self.__dict__.copy()
        
        if type(remove) == list and remove != None:
            for item in remove:
                if item in rdic.keys():
                    rdic.pop(item)
        elif remove != None and remove in rdic.keys():
            rdic.pop(remove)
        
        return rdic
    
    def getCopyOfSelf(self):
        """ returns a copy of self """
        copy = Attribute()
        for item in self.__dict__.keys():
            copy.addAttribute(item, self.__dict__[item], True)
            
        return copy
    
    def __repr__(self):
        return "<General Attribute Node with (%d) lists and (%d) attributes>" % (len([item for item in self.__dict__.keys() if (type(self.__dict__[item]) == list) or (type(self.__dict__[item]) == tuple)]), (len(self.__dict__.keys()) - len([item for item in self.__dict__.keys() if (type(self.__dict__[item]) == list) or (type(self.__dict__[item]) == tuple)])))
