from Globals import _ENGINE_game_type

class Character(object):
    def __init__(self):
        self.name = "New Character"
        
        # EVE Style or D&D?
        if _ENGINE_game_type == "EVE Style":
            starting_attribute = 8 # max 30, logorithmic 
        elif _ENGINE_game_type == "D&D Style":
            starting_attribute = 7 # max 18, or 18 + 100% from 19 to 25 on expanded rules
        elif _ENGINE_game_type == "Fallout Style":
            starting_attribute = 5 # max 10
        
        self.intellegence = self.charisma = self.perception = self.willpower = self.memory = starting_attribute
        self.luck = 5 # default luck, out of a 100 percetage
        
        self.experience = 0
        self.level = 0
        self.rank = 0
        self.profession = "Mingebag"
        
        # Position, x, y, z
        self.position = [10,10,0] # Within the region
        self.region = [0,0,0] # Within the world
        self.universe = [0,0,0] # Within the universe
    
    def __repr__(self):
        return "<Character %s>" % self.name
    
    def getPosition(self, position, style):
        '''
        slots
            0: Regional position
            1: World Position
            2: Universal position
        Style
            0: (x,y)
            1: (x,z)
            2: (y,z)
            3: (x,y,z)
        '''
        if style == 0:
            style = [0,1]
        elif style == 1:
            style = [0,2]
        elif style == 2:
            style = [1,2]
        elif style == 3:
            style = [0,1,2]
        
        if position == 0:
            position = self.position
        elif position == 1:
            position = self.region
        elif position == 2:
            position = self.universe
        
        returnposition = []
        
        for slice in style:
            returnposition.append(position[slice])
        
        return tuple(returnposition)
        