
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
    def __init__(self, name, **kws):
        '''At least the name is required for the character to be generated'''
        
        self.name = name
        self.ready = False # waiting on all the skill parsing to be finished
        
        # Start everything off as None to reduce the else statements
        intellegence = None
        memory = None
        perception = None
        willpower = None
        charisma = None
        self.characterID = None
        self.race = None
        self.bloodline = None
        self.gender = None
        self.corporationName = None
        self.corporationID = None
        self.cloneName = None
        self.cloneSkillPoints = None
        self.balance = None
        self.timeUpdated = None
        self.currentlyTraining = None
        
        if kws.has_key("characterID") and kws["characterID"]:
            self.characterID = int(kws["characterID"])
            
        if kws.has_key("race") and kws["race"]:
            self.race = kws["race"]
            
        if kws.has_key("bloodline") and kws["bloodline"]:
            self.bloodline = kws["bloodline"]
            
        if kws.has_key("gender") and kws["gender"]:
            self.gender = kws["gender"]
            
        if kws.has_key("corporationName") and kws["corporationName"]:
            self.corporationName = kws["corporationName"]
            
        if kws.has_key("corporationID") and kws["corporationID"]:
            self.corporationID = int(kws["corporationID"])
            
        if kws.has_key("cloneName") and kws["cloneName"]:
            self.cloneName = kws["cloneName"]
            
        if kws.has_key("cloneSkillPoints") and kws["cloneSkillPoints"]:
            self.cloneSkillPoints = int(["cloneSkillPoints"])
            
        if kws.has_key("balance") and kws["balance"]:
            self.balance = int(kws["balance"])
            
        if kws.has_key("timeUpdated") and kws["timeUpdated"]:
            self.timeUpdated = kws["timeUpdated"]
            
        if kws.has_key("currentlyTraining") and kws["currentlyTraining"]:
            self.currentlyTraining = kws["currentlyTraining"]
        
        # This set of information must be run through their edit methods manually at the moment
        self.augmentations = {}
        self.skillset = {}
        self.certificates = {}
        self.corporationRoles = {}
        self.corporationRolesAtHQ = {}
        self.corporationRolesAtBase = {}
        self.corporationRolesAtOther = {}
        self.corporationTitles = {}
        
        if kws.has_key("intellegence") and kws["intellegence"]:
            intellegence = kws['intellegence']
            
        if kws.has_key("memory") and kws["memory"]:
            memory = kws["memory"]
            
        if kws.has_key("perception") and kws["perception"]:
            perception = kws["perception"]
            
        if kws.has_key("willpower") and kws["willpower"]:
            willpower = kws["willpower"]
            
        if kws.has_key("charisma") and kws["charisma"]:
            charisma = kws["charisma"]
        
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
        '''Builds the level0-5 attributes for %s''' % self.name
        for level in range(6):
            self.__setattr__("level%s" % level, self.getSkillsAtLevel(level))
    
    def addSkill(self, skill):
        if skill not in self.skillset:
            self.skillset[skill.id] = skill
            self.totalSkillPoints += skill.skillpoints
            self.buildLevels()
        else:
            print "Please either edit the skill in place or delete it before adding it again"

    def editSkill(self, id, **kw):
        '''
        name is an option if added a new skill to the character, will be passed through to building the skill\n
        you should never have to delete a skill from your tree, but incase CCP does something strange
        '''
        id = int(id)
        if id in self.skillset:
            if kw.has_key('skillpoints') and kw['skillpoints']:
                self.totalSkillPoints -= self.skillset[id].skillpoints # remove the current points
                self.skillset[id].skillpoints = kw['skillpoints']
                self.totalSkillPoints += kw['skillpoints'] # add the new amount back in
            
            if kw.has_key('level') and kw['level']:
                self.skillset[id].level = kw['level']
                
            if kw.has_key('name') and kw['name']:
                self.skillset[id].name = kw['name']
                
            if kw.has_key('rank') and kw['rank']:
                self.skillset[id].rank = kw['rank']
                
            if kw.has_key('primary') and kw['primary']:
                self.skillset[id].primary = kw['primary']
                
            if kw.has_key('secondary') and kw['secondary']:
                self.skillset[id].secondary = kw['secondary']
                
            if kw.has_key('grouname') and kw['grouname']:
                self.skillset[id].groupname = kw['grouname']
                
            if kw.has_key('groupid') and kw['groupid']:
                self.skillset[id].groupid = kw['groupid']
                
            if kw.has_key('description') and kw['description']:
                self.skillset[id].description = kw['description']
        
            self.buildLevels()
        else:
            print "Skill does not exist in set"
    
    def deleteSkill(self, id):
        id = int(id)
        if id in self.skillset:
            self.totalSkillPoints -= self.skillset[id].skillpoints
            self.skillset.pop(id)
        else:
            print "Skill does not exist in set"
    
    def getSkill(self, id):
        for skill in self.skillset:
            if skill == id:
                return skill
        return None
    
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
    
    def setCurrentlyTraining(self, skill):
        '''
            Only takes an object of the Skill class
        '''
        self.currentlyTraining = skill
