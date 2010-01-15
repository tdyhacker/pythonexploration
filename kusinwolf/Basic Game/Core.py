import os, sys
from Character import Character
from Globals import *

# (Was) Just the Engine mechanics

class Physics(object):
    def __init__(self):
        # Global Settings
        # I'm kin to HL2 here :)
        self.gravity = 600
        

class Engine(object):
    def __init__(self):
        """Engine is called when the program starts.
           it initializes everything it needs.
        """
        
        # Starting Physics Engine
        self.physics = Physics()
        
        self.game = Game()
        
        self.connected = {}
        self.connections = 0

    def addCharacter(self):
        self.connections += 1 # This is being used as the server id for now, but needs to be something more unique
        self.connected[self.connections] = Character(self.game, self.engine, server_id = self.connections, position = self.game.getDefaultStartingPosition(), default_attributes = self.game.getDefaultAttributesValue(), )

class Game(object):
    def __init__(self):
        '''
            Everything should be modified here for making the game act like you want it to
        '''
        
        # For now
        self.game_max_level = 10
        self.game_max_rank = 5
        self.game_max_attributes = 30
    
    def getDefaultCharacterProfession(self):
        return "Mingebag"
    
    def getDefaultAttributesValue(self):
        return 7
    
    def getDefaultStartingPosition(self):
        return (0,0,0)