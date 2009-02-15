from re import compile

# TODO: Add threading to speed up processing
#	- API call thread
#	- Parse thread

class Skill(object):
    def __init__(self, id, skillpoints, level, name=None):
        '''skill id, skillpoints and level required, name is optional'''
        self.id = int(id)
        self.skillpoints = int(skillpoints)
        self.level = int(level)
        self.name = name or "Unknown"

        self.level1rank1 = 250      # 250
        self.level2rank1 = 1415     # 1,415
        self.level3rank1 = 8000     # 8,000
        self.level4rank1 = 45255    # 45,255
        self.level5rank1 = 256000   # 256,000

        # Need to remove this and replace it with the true ranks, this method does not work for anything that has more skillpoints then the start
        if self.level == 1:
            self.rank = int(self.skillpoints / self.level1rank1)
        elif self.level == 2:
            self.rank = int(self.skillpoints / self.level2rank1)
        elif self.level == 3:
            self.rank = int(self.skillpoints / self.level3rank1)
        elif self.level == 4:
            self.rank = int(self.skillpoints / self.level4rank1)
        elif self.level == 5:
            self.rank = int(self.skillpoints / self.level5rank1)
    
    def __repr__(self):
        return "<Skill %s - Points %s - Level %s - Rank: %s>" % (self.name, self.skillpoints, self.level, self.rank)

    def __cmp__(self, right):
        if type(right) == int:
            return cmp(self.skillpoints, right)
        else:
            return cmp(self.skillpoints, right.skillpoints)

    def nextLevel(self):
        if self.level != 5:
            return (self.__getattribute__("level%srank1" % (self.level + 1)) * self.rank) - self.skillpoints
        else:
            return 0

class Certificate(object):
    def __init__(self, id, level=None, name=None):
        '''id is required, level is unknown at the moment, name is unknown at the moment'''
        self.id = int(id)
        self.level = level or "Unknown"
        self.name = name or "Unknown"
    
    def __repr__(self):
        return "<Certificate %s>" % self.name

class Augmentation(object):
    def __init__(self, name, value, slot):
        '''slot is not well defined'''
        self.name = name
        self.value = int(value)
        self.slot = int(slot)
    
    def __repr__(self):
        return "<Augmentation Slot%s: %s +%s>" % (self.slot, self.name, self.value)

class Role(object):
    def __init__(self, id, name):
        self.id = int(id)
        self.name = name
    
    def __repr__(self):
        return "<Role %s>" % self.name

class Title(Role):
    # exactly the same as Role
    def __repr__(self):
        return "<Title %s>" % self.name

class Character(object):
    def __init__(self, name, characterID=None,
                 race=None, bloodline=None, gender=None, corporationName=None, corporationID=None,
                 cloneName=None, cloneSkillPoints=None, balance=None, timeUpdated=None, intellegence=None,
                 memory=None, perception=None, willpower=None, charisma=None):
        '''At least the name is required for the character to be generated'''
        
        if characterID:
            characterID = int(characterID)
        if corporationID:
            corporationID = int(corporationID)
        if cloneSkillPoints:
            cloneSkillPoints = int(cloneSkillPoints)
        if balance:
            balance = int(balance)
            
        self.characterID = characterID
        self.name = name
        self.race = race
        self.bloodline = bloodline
        self.gender = gender
        self.corporationName = corporationName
        self.corporationID = corporationID
        self.cloneName = cloneName
        self.cloneSkillPoints = cloneSkillPoints
        self.balance = balance
        self.timeUpdated = timeUpdated
        
        # This set of information must be run through their edit methods manually at the moment
        self.augmentations = {}
        self.skillset = {}
        self.certificates = {}
        self.corporationRoles = {}
        self.corporationRolesAtHQ = {}
        self.corporationRolesAtBase = {}
        self.corporationRolesAtOther = {}
        self.corporationTitles = {}
        
        # Edit attributes if any
        self.attributes(intellegence, memory, perception, willpower, charisma)
        
        # Changeable
        self.totalSkillPoints = 0
    
    def __repr__(self):
        temp = str(self.totalSkillPoints)
        sp = ""
        count = len(temp)
        for char in temp:
            if count % 3 == 0 and count != len(temp):
                sp += ","
            count -= 1
            sp += char
        
        temp = str(self.balance)
        bal = ""
        count = len(temp)
        for char in temp:
            if count % 3 == 0 and count != len(temp) and count > 0 and char != ".":
                bal += ","
            if char == ".":
                count = 0 # prevent more commas
            count -= 1
            bal += char
        
        return "<Character %s - Skillpoints: %s - Balance: %s>" % (self.name, sp, bal)
    
    def attributes(self, intellegence, memory, perception, willpower, charisma):
        '''The attributes of the character without any enhancements from implants or skills'''
        if intellegence:
            intellegence = int(intellegence)
        if memory:
            memory = int(memory)
        if perception:
            perception = int(perception)
        if willpower:
            willpower = int(willpower)
        if charisma:
            charisma = int(charisma)
        
        self.intellegence = intellegence
        self.memory = memory
        self.perception = perception
        self.willpower = willpower
        self.charisma = charisma
    
    def getSkillsAtLevel(self, level):
        if level > 5:
            return "Error: No skill greater than 5"
        elif level < 0:
            return "Error: Unable to gather skills that are not currently trained [Functionality to arrive in the future]"
        else:
            slist = []
            for skill in self.skillset:
                if self.skillset[skill].level == level:
                    slist.append(self.skillset[skill])
            return slist

    def buildLevels(self):
        '''Builds the level1-5 attributes for %s''' % self.name
        for level in range(6):
            self.__setattr__("level%s" % level, self.getSkillsAtLevel(level))

    def editSkill(self, id, skillpoints, level, name=None, delete=False):
        '''
        editing a non existent skill is the same as adding\n
        name is an option if added a new skill to the character, will be passed through to building the skill\n
        you should never have to delete a skill from your tree, but incase CCP does something strange
        '''
        id = int(id)
        if delete:
            self.totalSkillPoints -= self.skillset[id].skillpoints
            self.skillset.pop(id)
        elif id in self.skillset:
            self.totalSkillPoints -= self.skillset[id].skillpoints
            self.skillset[id].skillpoints = skillpoints
            self.skillset[id].level = level
            self.skillset[id].name = name
        else:
            self.skillset[id] = Skill(id, skillpoints, level, name)
            self.totalSkillPoints += self.skillset[id].skillpoints
        
        self.buildLevels()
    
    def editAugmentation(self, slot, name, value, delete=False):
        '''
        editing a non existent skill is the same as adding\n
        All the implants in the clone's head currently
        '''
        if delete:
            self.augmentations.pop(int(slot))
        elif slot in self.augmentations:
            self.augmentations[slot].name = name
            self.augmentations[slot].value = int(value)
        else:
            self.augmentations[slot] = Augmentation(name, int(value), int(slot))
    
    def editCertificate(self, id, level=None, name=None, delete=False):
        '''
        editing a non existent certificate is the same as adding\n
        name and level are currently unknown\n
        you should never have to delete a certificate from your tree, but incase CCP does something strange
        '''
        id = int(id)
        if delete:
            self.certificates.pop(id)
        elif id in self.certificates:
            self.certificates[id].level = level
            self.certificates[id].name = name
        else:
            self.certificates[id] = Certificate(id, level, name)
    
    def editCorporationRoles(self, id, rolename=None, delete=False):
        '''
        editing a non existent role is the same as adding\n
        pass True through the delete flag to remove the item
        '''
        id = int(id)
        if delete:
            self.corporationRoles.pop(id)
        elif id in self.certificates:
            self.corporationRoles[id].name = name
        else:
            self.corporationRoles[id] = Role(id, name)

    def editCorporationRolesAtHQ(self, id, rolename=None, delete=False):
        '''
        editing a non existent role is the same as adding\n
        pass True through the delete flag to remove the item
        '''
        id = int(id)
        if delete:
            self.corporationRolesAtHQ.pop(id)
        elif id in self.certificates:
            self.corporationRolesAtHQ[id].name = name
        else:
            self.corporationRolesAtHQ[id] = Role(id, name)

    def editCorporationRolesAtBase(self, id, rolename=None, delete=False):
        '''
        editing a non existent role is the same as adding\n
        pass True through the delete flag to remove the item
        '''
        id = int(id)
        if delete:
            self.corporationRolesAtBase.pop(id)
        elif id in self.certificates:
            self.corporationRolesAtBase[id].name = name
        else:
            self.corporationRolesAtBase[id] = Role(id, name)
    
    def editCorporationRolesAtOther(self, id, rolename=None, delete=False):
        '''
        editing a non existent role is the same as adding\n
        pass True through the delete flag to remove the item
        '''
        id = int(id)
        if delete:
            self.corporationRolesAtOther.pop(id)
        elif id in self.certificates:
            self.corporationTitles
            self.corporationRolesAtOther[id].name = name
        else:
            self.corporationRolesAtOther[id] = Role(id, name)

    def editCorporationTitles(self, id, rolename=None, delete=False):
        '''
        editing a non existent title is the same as adding\n
        pass True through the delete flag to remove the item
        '''
        id = int(id)
        if delete:
            self.corporationTitles.pop(id)
        elif id in self.certificates:
            self.corporationTitles[id].name = name
        else:
            self.corporationTitles[id] = Title(id, name)

def extractXML(filename):
    '''
    filename is the string in which the file is located on the hard disk\n
    returns a characterobject
    '''
    
    timeUpdated = None
    characterID = None
    augmentorName = None
    characterobject = None
    slot = 1
    
    try:
        characterSheet = open(filename, "r")
    except:
        print "File not exist in location %s" % filename
        characterSheet.close()
    
    for line in characterSheet.readlines():
        if compile(""".*<currentTime>(.*)</currentTime>.*""").match(line):
            timeUpdated = compile(""".*<currentTime>(.*)</currentTime>.*""").match(line).groups()[0]
        
        if compile(""".*<characterID>(.*)</characterID>.*""").match(line):
            characterID = compile(""".*<characterID>(.*)</characterID>.*""").match(line).groups()[0]
        
        if compile(""".*<name>(.*)</name>.*""").match(line):
            characterobject = Character(compile(""".*<name>(.*)</name>.*""").match(line).groups()[0], characterID=characterID, timeUpdated=timeUpdated)
        
        if compile(""".*<race>(.*)</race>.*""").match(line):
            characterobject.race = compile(""".*<race>(.*)</race>.*""").match(line).groups()[0]
        
        if compile(""".*<bloodLine>(.*)</bloodLine>.*""").match(line):
            characterobject.bloodline = compile(""".*<bloodLine>(.*)</bloodLine>.*""").match(line).groups()[0]
        
        if compile(""".*<gender>(.*)</gender>.*""").match(line):
            characterobject.gender = compile(""".*<gender>(.*)</gender>.*""").match(line).groups()[0]
        
        if compile(""".*<corporationName>(.*)</corporationName>.*""").match(line):
            characterobject.corporationName = compile(""".*<corporationName>(.*)</corporationName>.*""").match(line).groups()[0]
        
        if compile(""".*<corporationID>(.*)</corporationID>.*""").match(line):
            characterobject.corporationID = compile(""".*<corporationID>(.*)</corporationID>.*""").match(line).groups()[0]
        
        if compile(""".*<cloneName>(.*)</cloneName>.*""").match(line):
            characterobject.cloneName = compile(""".*<cloneName>(.*)</cloneName>.*""").match(line).groups()[0]
        
        if compile(""".*<cloneSkillPoints>(.*)</cloneSkillPoints>.*""").match(line):
            characterobject.cloneSkillPoints = compile(""".*<cloneSkillPoints>(.*)</cloneSkillPoints>.*""").match(line).groups()[0]
        
        if compile(""".*<balance>(.*)</balance>.*""").match(line):
            characterobject.balance = compile(""".*<balance>(.*)</balance>.*""").match(line).groups()[0]
        
        if compile(""".*<augmentatorName>(.*)</augmentatorName>.*""").match(line):
            augmentorName = compile(""".*<augmentatorName>(.*)</augmentatorName>.*""").match(line).groups()[0]
        
        if compile(""".*<augmentatorValue>(.*)</augmentatorValue>.*""").match(line):
            characterobject.editAugmentation(slot, augmentorName, compile(""".*<augmentatorValue>(.*)</augmentatorValue>.*""").match(line).groups()[0])
            slot += 1
        
        if compile(""".*<intelligence>(.*)</intelligence>.*""").match(line):
            characterobject.intelligence = compile(""".*<intelligence>(.*)</intelligence>.*""").match(line).groups()[0]
        
        if compile(""".*<memory>(.*)</memory>.*""").match(line):
            characterobject.memory = compile(""".*<memory>(.*)</memory>.*""").match(line).groups()[0]
        
        if compile(""".*<charisma>(.*)</charisma>.*""").match(line):
            characterobject.charisma = compile(""".*<charisma>(.*)</charisma>.*""").match(line).groups()[0]
        
        if compile(""".*<perception>(.*)</perception>.*""").match(line):
            characterobject.perception = compile(""".*<perception>(.*)</perception>.*""").match(line).groups()[0]
        
        if compile(""".*<willpower>(.*)</willpower>.*""").match(line):
            characterobject.willpower = compile(""".*<willpower>(.*)</willpower>.*""").match(line).groups()[0]
        
        if compile(""".*<row typeID="(.*)" skillpoints="(.*)" level="(.*)" />.*""").match(line):
            skillInfo = compile(""".*<row typeID="(.*)" skillpoints="(.*)" level="(.*)" />.*""").match(line).groups()
            characterobject.editSkill(skillInfo[0], skillInfo[1], skillInfo[2])
        
        if compile(""".*<row certificateID="(.*)" />.*""").match(line):
            characterobject.editCertificate(compile(""".*<row certificateID="(.*)" />.*""").match(line).groups()[0])
        
        # if the rowset name is in a certain area, change the function being used.match(line)
        if compile(""".*<rowset name="(.*)" key=".*" columns=".*">.*""").match(line):
            row = compile(""".*<rowset name="(.*)" key=".*" columns=".*">.*""").match(line)
        
        if compile(""".*<row roleID="(.*)" roleName="(.*)" />.*""").match(line):
            roleInfo = compile(""".*<row roleID="(.*)" roleName="(.*)" />.*""").match(line).groups()
            
            if row == "corporationRoles":
                characterobject.corporationRoles(roleInfo[0], roleInfo[1])
            elif row == "corporationRolesAtHQ":
                characterobject.corporationRolesAtHQ(roleInfo[0], roleInfo[1])
            elif row == "corporationRolesAtBase":
                characterobject.corporationRolesAtBase(roleInfo[0], roleInfo[1])
            elif row == "corporationRolesAtOther":
                characterobject.corporationRolesAtOther(roleInfo[0], roleInfo[1])
        
        if compile(""".*<row titleID="(.*)" titleName="(.*)" />.*""").match(line):
            titleInfo = compile(""".*<row titleID="(.*)" titleName="(.*)" />.*""").match(line).groups()
            characterobject.corporationRoles(titleInfo[0], titleInfo[1])

    characterSheet.close()
    
    return characterobject

def extractAPI(APIKey):
    '''
    a key is required to connect to the API
    returns a characterobject
    '''
    # TODO: Connect to API at eve-online to gather information
    return "Fixing this functionality soon"
