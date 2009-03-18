class Character(object):
    def __init__(self):
        self.name = "Bob"
        # Add Attributes
    
    def __repr__(self):
        return "<Character %s>" % self.name