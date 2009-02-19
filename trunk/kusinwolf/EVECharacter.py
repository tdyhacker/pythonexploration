from re import compile
import httplib, urllib
import wx

# TODO: Add threading to speed up processing
#	- API call thread
#	- Parse thread
#       - Use MySQL database to keep track of skilltree to reduce API calls

SKILLTREE = {}

class Skill(object):
    def __init__(self, id, skillpoints, level, name=None, rank=None, primary=None, secondary=None, groupname=None, groupid=None, description=None, dependencies=None):
        '''skill id, skillpoints and level required, name is optional'''
        self.id = int(id)
        self.skillpoints = int(skillpoints)
        self.level = int(level)
        self.name = name or "Unknown"
        if rank:
            rank = int(rank)
        self.rank = rank
        self.primary = primary
        self.secondary = secondary
        self.groupname = groupname
        self.groupid = groupid
        self.description = description
        self.dependencies = dependencies # Needs to be a list, will then be turned into a dictionary later one

        # What it takes to hit this level
        self.level1rank1 = 250      # 250
        self.level2rank1 = 1415     # 1,415
        self.level3rank1 = 8000     # 8,000
        self.level4rank1 = 45255    # 45,255
        self.level5rank1 = 256000   # 256,000
    
    def __repr__(self):
        return "<Skill %s - Points %s - Level %s - Rank %sx>" % (self.name, self.skillpoints, self.level, self.rank)

    def __cmp__(self, right):
        if type(right) == int:
            return cmp(self.skillpoints, right)
        else:
            return cmp(self.skillpoints, right.skillpoints)
    
    def printable(self):
        if len(self.name) >= 25:
            return "%s\t%s\t\t%sx" % (self.name, self.skillpoints, self.rank)
        elif len(self.name) >= 19:
            return "%s\t\t%s\t\t%sx" % (self.name, self.skillpoints, self.rank)
        elif len(self.name) >= 14:
            return "%s\t\t\t%s\t\t%sx" % (self.name, self.skillpoints, self.rank)
        elif len(self.name) >= 9:
            return "%s\t\t\t\t%s\t\t%sx" % (self.name, self.skillpoints, self.rank)
        else:
            return "%s\t\t\t\t\t%s\t\t%sx" % (self.name, self.skillpoints, self.rank)

    def nextLevel(self):
        if self.level != 5:
            return (self.__getattribute__("level%srank1" % (self.level + 1)) * self.rank) - self.skillpoints
        else:
            return 0
    
    def expandedrepr(self):
        return "<Skill %s - Points %s - Level %s - Rank %sx\n\t- PrimaryAttribute %s - SecondaryAttribute %s\n\t- GroupName %s - GroupID %s\n\tDescription: %s>" % (
                    self.name, self.skillpoints, self.level, self.rank, self.primary, self.secondary, self.groupname, self.groupid, self.description)

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
    
    def addSkill(self, skill):
        if skill not in self.skillset:
            self.skillset[skill.id] = skill
            self.totalSkillPoints += skill.skillpoints
            self.buildLevels()

    def editSkill(self, id, skillpoints, level, name=None, rank=None, primary=None, secondary=None, groupname=None, groupid=None, description=None, delete=False):
        '''
        editing a non existent skill is not the same as adding\n
        name is an option if added a new skill to the character, will be passed through to building the skill\n
        you should never have to delete a skill from your tree, but incase CCP does something strange
        '''
        id = int(id)
        if delete:
            self.totalSkillPoints -= self.skillset[id].skillpoints
            self.skillset.pop(id)
        elif id in self.skillset:
            self.totalSkillPoints -= self.skillset[id].skillpoints # remove the current points
            self.skillset[id].skillpoints = skillpoints
            self.skillset[id].level = level
            self.skillset[id].name = name
            self.skillset[id].rank = rank
            self.skillset[id].primary = primary
            self.skillset[id].secondary = secondary
            self.skillset[id].groupname = grouname
            self.skillset[id].groupid = groupid
            self.skillset[id].description = description
            self.totalSkillPoints += self.skillset[id].skillpoints # add the new amount back in
        
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
            characterobject.addSkill(Skill(skillInfo[0], skillInfo[1], skillInfo[2]))
        
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

def extractAPI(params):
    '''
    a key is required to connect to the API
    returns a characterobject
    '''
    timeUpdated = None
    characterID = None
    augmentorName = None
    characterobject = None
    slot = 1

    charactersheet = apiSelect("charactersheet", params)
    
    buildSkillTree(params)
    
    data = charactersheet.read()
    
    for line in data.split("\r\n"):
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
            id = int(skillInfo[0])
            skillpoints = int(skillInfo[1])
            level = int(skillInfo[2])
            
            if str(id) in SKILLTREE:
                SKILLTREE[str(id)].skillpoints = skillpoints
                SKILLTREE[str(id)].level = level
                characterobject.addSkill(SKILLTREE[str(id)])
            else:
                characterobject.addSkill(Skill(id, skillpoints, level)) # , name=SKILLTREE[id].name, rank=SKILLTREE[id].rank, description=SKILLTREE[id].description
        
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

    return characterobject

def buildSkillTree(params):
    '''
    :D Get up everybody, lets get to the disco\n
    Oh Baby! I'm king of disco! :D
    '''
    rank = None
    primary = None
    secondary = None
    name = None
    id = None
    groupname = None
    groupid = None
    description = ""
    required = []
    isdescription = False
    
    tree = apiSelect("skilltree", params)

    skills = tree.read()
    for sline in skills.split("\r\n"): # While not found and not end of data
        pgroupname_groupid = compile(""".*<row groupName="(.*)" groupID="(.*)">.*""").match(sline)
        pname_groupid_id = compile(""".*<row typeName="(.*)" groupID=".*" typeID="(.*)">.*""").match(sline)
        
        if compile(""".*<description>.*""").match(sline):
            pisdescription = True
        if isdescription:
            description += sline
        if compile(""".*</description>.*""").match(sline):
            pisdescription = False
            
        prank = compile(""".*<rank>(.*)</rank>.*""").match(sline)
        prequired = compile(""".*<row typeID="(.*)" skillLevel=".*"/>.*""").match(sline)
        pprimary = compile(""".*<primaryAttribute>(.*)</primaryAttribute>.*""").match(sline)
        psecondary = compile(""".*<secondaryAttribute>(.*)</secondaryAttribute>.*""").match(sline)
        
        if pgroupname_groupid:
            groupname = pgroupname_groupid.groups()[0]
            groupid = pgroupname_groupid.groups()[1]
        if pname_groupid_id:
            name = pname_groupid_id.groups()[0]
            id = pname_groupid_id.groups()[1]
        if prank:
            rank = prank.groups()[0]
        if prequired:
            required.append(prequired.groups()[0])
        if pprimary:
            primary = pprimary.groups()[0]
        if psecondary:
            secondary = psecondary.groups()[0]
        
        if secondary: # Last object to be built
            SKILLTREE[id] = Skill(id, 0, 0, name=name, rank=rank, primary=primary, secondary=secondary, groupname=groupname, groupid=groupid, description=description, dependencies=required)
            # Reset everything
            rank = None
            primary = None
            secondary = None
            name = None
            id = None
            description = ""
            required = []
            isdescription = False
            
    
    # Rebuild skill dependencies for each skill so that they are objects in a dictionary, for greater indexing
    for skill in SKILLTREE:
        if SKILLTREE[skill]:
            requiredSkillsList = SKILLTREE[skill].dependencies
            SKILLTREE[skill].dependencies = {}
            for requiredSkill in requiredSkillsList:
                SKILLTREE[skill].dependencies[requiredSkill] = SKILLTREE[requiredSkill]

def apiSelect(item, params):
    '''Options:\n
        \tWalletTransactions    : requires full API key\n
        \tCharacterSheet        : Returns the current character sheet\n
        \tSkillInTraining       : Returns the current skill trainning, 0 for no skill\n
        \tSkillTree             : Returns the entire skill tree for EVE\n
        \tRefTypes              : Returns the reference types for the wallet\n
    '''

    params = urllib.urlencode( params )
    
    # connect to server, POST our request, fairly simple stuff...
    headers = { "Content-type": "application/x-www-form-urlencoded" }
    conn = httplib.HTTPConnection("api.eve-online.com")
    
    item = item.lower()
    
    if item == "wallettransactions":
        conn.request("POST", "/char/WalletTransactions.xml.aspx", params, headers) # Requires full API key
    elif item == "charactersheet":
        conn.request("POST", "/char/CharacterSheet.xml.aspx", params, headers)
    elif item == "skillintraining":
        conn.request("POST", "/char/SkillInTraining.xml.aspx", params, headers)
    elif item == "skilltree":
        conn.request("POST", "/eve/SkillTree.xml.aspx", params, headers) # no real inputs required
    elif item == "reftypes":
        conn.request("POST", "/eve/RefTypes.xml.aspx", params, headers) # no real inputs required
    
    response = conn.getresponse()

    conn.close
    
    return response


###################
# wxPython Window #
###################

# Tutorial
#http://zetcode.com/wxpython/

ID_QUIT = 1
ID_LEVEL1 = 100
ID_LEVEL2 = 101
ID_LEVEL3 = 102
ID_LEVEL4 = 103
ID_LEVEL5 = 104

class BottomPanel(wx.Panel):
    def __init__(self, parent, id, cObject):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        
        self.cObject = cObject # Character Object
        
        skillNamePanel = wx.Panel(self, -1, (5, 64))
        skillPointsPanel = wx.Panel(self, -1)
        rankPanel = wx.Panel(self, -1)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        # Add(item, proportion percentage, flags, border size)
        hbox.Add(skillNamePanel, 10, wx.EXPAND | wx.ALL, 5)
        hbox.Add(skillPointsPanel, 3, wx.EXPAND | wx.ALL, 5)
        hbox.Add(rankPanel, 2, wx.EXPAND | wx.ALL, 5)
        
        self.skillname = wx.StaticText(skillNamePanel, -1, 'Skill', (0, 0))
        self.skillpoints = wx.StaticText(skillPointsPanel, -1, '0', (0, 0))
        self.rank = wx.StaticText(rankPanel, -1, '0x', (0, 0))
        
        self.SetSizer(hbox)
    
    def DisplayLevel(self, level):
        skillnamelist = "SkillName at Level %s\n" % level
        skillpointslist = "SkillPoints\n"
        ranklist = "Rank\n"
        
        for skill in self.cObject.__getattribute__("level%s" % level):
            skillnamelist += str(skill.name) + "\n"
            skillpointslist += str(skill.skillpoints) + "\n"
            ranklist += str(skill.rank) + "x\n"

        self.skillname.SetLabel(skillnamelist)
        self.skillpoints.SetLabel(skillpointslist)
        self.rank.SetLabel(ranklist)

class Browser(wx.Frame):
    def __init__(self, parent, id, title, cObject, size=(400, 1024)):
        self.cObject = cObject # ChacterObject passed in
        # The entire window
        wx.Frame.__init__(self, parent, id, title, size) # Width, Height
        # A chunk of the GUI inside the frame
        panel = wx.Panel(self, -1)
        
        self.bottompanel = BottomPanel(panel, -1, cObject)
        
        # Menu information
        menubar = wx.MenuBar() # Creates the full menu bar
        file = wx.Menu() # Creates the file menu
        
        # Builds quit MenuItem in AppendItem
        file.AppendItem(wx.MenuItem(file, ID_QUIT, '&Quit\tCtrl+Q')) # Appends Quit option to File menu
        
        menubar.Append(file, '&File') # Adds File Menu to the full menu bar
        self.SetMenuBar(menubar) # Builds the menubar
        
        # Binds a user generated event to the OnQuit method
        self.Bind(wx.EVT_MENU, self.OnQuit, id=1)
        
        # Grabbing font
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        
        # Building mutable inner box, like a div or table
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Build row inside mutable box
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Creates static text
        stext = wx.StaticText(panel, -1, 'Character Name:')
        stext.SetFont(font)
        
        # adds it to the horizontal box
        hbox1.Add(stext, 0, wx.RIGHT, 8)
        
        # Creates static text
        stext = wx.StaticText(panel, -1, self.cObject.name)
        stext.SetFont(font)
        
        # adds it to the horizontal box
        hbox1.Add(stext, 1)
        vbox.Add(hbox1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        
        # Spacer
        vbox.Add((-1,10))
        
        # Creating buttons
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        
        btn = wx.Button(panel, ID_LEVEL1, 'Level 1', size=(70, 30))
        hbox5.Add(btn, 0)
        
        btn = wx.Button(panel, ID_LEVEL2, 'Level 2', size=(70, 30))
        hbox5.Add(btn, 0, wx.LEFT , 5)
        
        btn = wx.Button(panel, ID_LEVEL3, 'Level 3', size=(70, 30))
        hbox5.Add(btn, 0, wx.LEFT, 5)
        
        btn = wx.Button(panel, ID_LEVEL4, 'Level 4', size=(70, 30))
        hbox5.Add(btn, 0, wx.LEFT, 5)
        
        btn = wx.Button(panel, ID_LEVEL5, 'Level 5', size=(70, 30))
        hbox5.Add(btn, 0, wx.LEFT, 5)
        
        vbox.Add(hbox5, 0, wx.ALIGN_CENTER | wx.CENTER, 10)
        
        # Binds a user generated event to the OnQuit method
        self.Bind(wx.EVT_BUTTON, self.OnLevel1, id=ID_LEVEL1)
        self.Bind(wx.EVT_BUTTON, self.OnLevel2, id=ID_LEVEL2)
        self.Bind(wx.EVT_BUTTON, self.OnLevel3, id=ID_LEVEL3)
        self.Bind(wx.EVT_BUTTON, self.OnLevel4, id=ID_LEVEL4)
        self.Bind(wx.EVT_BUTTON, self.OnLevel5, id=ID_LEVEL5)
        
        # Spacer
        vbox.Add((-1,10))
        
        vbox.Add(self.bottompanel, 1, wx.EXPAND | wx.ALL, 5)
        
        # Sets the sizer object
        panel.SetSizer(vbox)

        # Centers on the screen
        self.Centre()
        
        self.SetSize(size) # Adjust size after the Sizer has been built
        
        # Keeps the window visable to the human
        self.Show(True)
        
        #panel.SetSize((400,400)) Is this even used?
    
    def OnLevel1(self, event):
        self.bottompanel.DisplayLevel(1)
    
    def OnLevel2(self, event):
        self.bottompanel.DisplayLevel(2)
    
    def OnLevel3(self, event):
        self.bottompanel.DisplayLevel(3)
    
    def OnLevel4(self, event):
        self.bottompanel.DisplayLevel(4)

    def OnLevel5(self, event):
        self.bottompanel.DisplayLevel(5)
    
    def OnQuit(self, event):
        self.Close()
