class Character(object):
    def __init__(self, game, engine, server_id = None, experience = 0, level = 0, rank = 0, profession = None, default_attributes = 0, name = "New Character", position = (0,0,0)):
        # Character Info
        self.name = name
        self.server_id = server_id
        
        self.game = game
        self.engine = engine
        
        # Character attributes
        self.intellegence = self.charisma = self.perception = self.willpower = self.memory = default_attributes
        self.experience = experience
        self.level = level
        self.rank = rank
        self.profession = profession
        
        # Character Position, x, y, z
        self.regionalPosition = position # Within the region
        self.worldlyPosition = position # Within the world
        self.universalPosition = position # Within the universe
    
    def __repr__(self):
        return "<Character %s>" % self.name
    
    def getRegionalPosition(self):
        '''
            Domains
                Regional position
                Worldly Position
                Universal position
        '''
        return self.regionalPosition
        
    def getWorldlyPosition(self):
        '''
            Domains
                Regional position
                Worldly Position
                Universal position
        '''
        return self.worldlyPosition
        
    def getUniversalPosition(self):
        '''
            Domains
                Regional position
                Worldly Position
                Universal position
        '''
        return self.universalPosition
    
    def getName(self):
        return self.name
    
    def getExperience(self):
        return self.name
    
    def getLevel(self):
        return self.level
    
    def getRank(self):
        return self.rank
    
    def getProfession(self):
        return self.profession
    
    def getIntellegence(self):
        return self.intellegence
    
    def getCharisma(self):
        return self.charisma
    
    def getPerception(self):
        return self.perception
    
    def getWillpower(self):
        return self.willpower
    
    def getMemory(self):
        return self.memory
    
    def setName(self, value):
        self.name = value
    
    def setExperience(self, value):
        self.name = value
    
    def setLevel(self, value):
        self.level = value
    
    def setRank(self, value):
        self.rank = value
    
    def setProfession(self, value):
        self.profession = value
    
    def setIntellegence(self, value):
        '''
            HAH, shame it's not this easy in reality! :P
        '''
        self.intellegence = value
    
    def setCharisma(self, value):
        '''
            HAH, shame it's not this easy in reality! :P
        '''
        self.charisma = value
    
    def setPerception(self, value):
        '''
            HAH, shame it's not this easy in reality! :P
        '''
        self.perception = value
    
    def setWillpower(self, value):
        '''
            HAH, shame it's not this easy in reality! :P
        '''
        self.willpower = value
    
    def setMemory(self, value):
        '''
            HAH, shame it's not this easy in reality! :P
        '''
        self.memory = value