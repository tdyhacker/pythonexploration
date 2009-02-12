from re import compile
from EVECharacter import *

def xmlExtract(filename):
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

lucitania = xmlExtract("Lucitania.xml")
xressmeth = xmlExtract("Xressmeth.xml")