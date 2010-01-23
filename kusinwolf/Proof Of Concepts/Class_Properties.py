#!/usr/bin/env python

"""
This proof of concept is just to display the new python 2.6 property overrides in classes
"""

class C(object):
    def __init__(self):
        self._x = "Not me!"
    
    @property
    def x(self):
        """Getter for self._x"""
        return self._x
    
    @x.setter
    def x(self, value):
        """Setter for self._x"""
        self._x = value
    
    @x.deleter
    def x(self):
        """Deconstructor for self._x"""
        self._x = "</life> x_x"


print "Creating obj out of class C"
obj = C()
print "Currently obj.x = ", obj.x
print "Assigning new value to obj.x"
obj.x = "Nothing to see here"
print "Now obj.x = ", obj.x
print "Deteling obj.x"
del obj.x
print "Lastly obj.x = ", obj.x