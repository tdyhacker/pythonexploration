#!/usr/bin/env python

"""
In this example, a Simple Single level inheritance is performed between two sets of classes, both with two attributes, a String and List
In the first set, the list is copied using the "[:]" extension of the list object to use a new memory space and copy the original list to it
as well as copying the hash table and tuple to prevent same memory sharing between instances of objects
In the second set, the list is simply a pointer to the entire inheritance tree that creates problems when using more than one instance of the sub class
the same problem occurs with a hash as well, but does not seem to affect a tuple

There can be some unquie power to having this form of inheritance, but for the majority of my work I have to fight with this problem consistently
and having a good explanation and example to clearify everything helps.
"""

# First Set
class One(object):
    """
    Parent Class
    """
    def __init__(self, name = "", var = [], tu = (), hash = {}):
        """
        This class should make copies of all the variable types
        """
        self.name = name
        self.vars = var[:] # Copy the list
        self.hash = hash.copy() # Copy the hash
        self.tu = tu[:] # Copy the tuple
        print self.name, "-", self.vars, self.tu, self.hash

class Two(One):
    """
    Child Class
    """
    def __init__(self, name = "", var = [], tu = (), hash = {}):
        One.__init__(self, name, var, tu, hash)

# Second Set
class Three(object):
    """
    Parent Class
    """
    def __init__(self, name = "", var = [], tu = (), hash = {}):
        """
        This class should not directly make copies of all the variable types
        """
        self.name = name
        self.vars = var # Point to list
        self.hash = hash # Point to the hash
        self.tu = tu # Point to the tuple
        print self.name, "-", self.vars, self.tu, self.hash

class Four(Three):
    """
    Child Class
    """
    def __init__(self, name = "", var = [], tu = (), hash = {}):
        Three.__init__(self, name, var, tu, hash)

print "New Instance of class Two()"
a = Two("The First")
print "Appending to a.vars list"
a.vars.append("In my List")
print "Adding item to a.hash"
a.hash['Hash1'] = 0
print "Appending to a.tu tuple"
a.tu = list(a.tu)
a.tu.append("Tuple Item 1")
a.tu = tuple(a.tu)

print "New Instance of class Two()"
b = Two("The Second") # Should have an empty list despite the value appened to a's list

print "\n"

print "New Instance of class Four()"
c = Four("The Thrid")
print "Appending to c.vars list"
c.vars.append("One item")
print "Adding item to c.hash"
c.hash['Hash1'] = 0
print "Appending to c.tu tuple"
c.tu = list(c.tu)
c.tu.append("Tuple Item 1")
c.tu = tuple(c.tu)

print "New Instance of class Four()"
d = Four("The Fourth") # Should have an empty list but now has what c has appened

print "\n"

# The interesting thing is when you provide a starter list, a new memory place is used and the problem goes away on it's own
# But the same can not be said for any hash objects, a new memory space has to be called for no matter what
print "== Now using startup variables within the initalization =="
print "New Instance of class Two()"
a = Two("The First", ['Starter Var',], tu = ("Beginning",), hash = {"one": 1})
print "Appending to a.vars list"
a.vars.append("In my List")
print "Adding item to a.hash"
a.hash['Hash2'] = 0
print "Appending to a.tu tuple"
a.tu = list(a.tu)
a.tu.append("Tuple Item 1")
a.tu = tuple(a.tu)

print "New Instance of class Two()"
b = Two("The Second") # Should have an empty list despite the value appened to a's list

print "\n"

print "New Instance of class Four()"
c = Four("The Thrid", ['Starter Var',], tu = ("Beginning",), hash = {"one": 1})
print "Appending to c.vars list"
c.vars.append("Two item")
print "Adding item to c.hash"
c.hash['Hash2'] = 0
print "Appending to c.tu tuple"
c.tu = list(c.tu)
c.tu.append("Tuple Item 1")
c.tu = tuple(c.tu)

# An interesting problem occurs here, this variable still retains the first instance of the class, which proves that the above variable instance is unique to everything else
print "New Instance of class Four()"
d = Four("The Fourth") # Should have an empty list but now has what c has appened