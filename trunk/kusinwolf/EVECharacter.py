class Skill(object):
    def __init__(self, id, skillpoints, level, name=None):
        '''skill id, skillpoints and level required, name is optional'''
        self.id = int(id)
        self.skillpoints = int(skillpoints)
        self.level = int(level)
        self.name = name or "Unknown"
    
    def __repr__(self):
        return "<Skill %s - Points %s - Level %s>" % (self.name, self.skillpoints, self.level)

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