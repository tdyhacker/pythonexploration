from re import compile
import httplib, urllib
import MySQLdb
from EVECharacter import Skill, Character, Certificate, Augmentation, Title
import threading
import time

# Required modules
# - easy_install mysql-python
# - sudo apt-get install python-wxgtk2.8

# TODO: Add threading to speed up processing
#	- API call thread
#	- Parse thread
#       - Use MySQL database to keep track of skilltree to reduce API calls
#       - Convert the current way of reading skills to SQL database
#       - Generate personal database to
#       - Add dependency table and cross reference table

# Notes:
# - Should the GUI even touch anything in the database?
# - If not, then a layer wrapper should be built to handle all functionality
# - That sounds too complicated for something this small

# SQL tables required for this script
#CREATE TABLE groups (id INT NOT NULL AUTO_INCREMENT, group_name TEXT, group_id INT, PRIMARY KEY(id));
#CREATE TABLE attribute (id INT NOT NULL AUTO_INCREMENT, attribute_name TEXT, PRIMARY KEY(id));
#CREATE TABLE skill (id INT NOT NULL AUTO_INCREMENT, skill_id INT, skill_name TEXT, rank INT, primary_attribute_id INT, secondary_attribute_id INT, groupname_id INT, description TEXT, PRIMARY KEY(id), FOREIGN KEY (groupname_id) REFERENCES groups(id), FOREIGN KEY (primary_attribute_id) REFERENCES attribute(id), FOREIGN KEY (secondary_attribute_id) REFERENCES attribute(id));

# SQL to grab the two attribute names and group names ordering first by group name and then by their ranks in order
#select s.skill_name, s.rank, a1.attribute_name primary_attribute, a2.attribute_name secondary_attribute, g.group_name group_name from skill s join attribute a1 on s.primary_attribute_id = a1.id join attribute a2 on s.secondary_attribute_id = a2.id join groups g on s.groupname_id = g.id order by s.groupname_id, s.rank;

DATABASE_NAME = "personal_db1" # Database to connect to
DATABASE_USER = "kusinwolf" # The name of the user with permission to connect
DATABASE_HOST = "localhost" # Location of the database, if it be online or somewhere else
DATABASE_PASSWORD = "" # Password to connect

TABLE_SKILL = "skill"
TABLE_GROUP = "groups"
TABLE_ATTRIBUTE = "attribute"

def _buildSkillTree(params):
    '''
        WARNING: This should only be run manually to build the entire database, not all the time
        
        Builds the entire skill tree in the MySQL database
        Currently manual labor of cleaning out the table is required
    '''
    info = {}
    info['required'] = []
    info['description'] = "" # There may not be a description
    
    # connection to the database
    if DATABASE_PASSWORD != "":
        db_conn = MySQLdb.connection(user=DATABASE_USER, db=DATABASE_NAME, host=DATABASE_HOST, password=DATABASE_PASSWORD)
    else:
        db_conn = MySQLdb.connection(user=DATABASE_USER, db=DATABASE_NAME, host=DATABASE_HOST)
    db_conn.autocommit(True)
    
    # Get the tree from the API
    tree = apiSelect("skilltree", params)    
    
    skills = tree.read()
    
    # For all the information in the API, go line by line
    for sline in skills.split("\r\n"): # While not found and not end of data
        pgroupname_groupid = compile(""".*<row groupName="(.*)" groupID="(.*)">.*""").match(sline)
        pname_groupid_id = compile(""".*<row typeName="(.*)" groupID=".*" typeID="(.*)">.*""").match(sline)
        
        pdescription = compile(""".*<description>(.*)</description>.*""").match(sline)
        prank = compile(""".*<rank>(.*)</rank>.*""").match(sline)
        prequired = compile(""".*<row typeID="(.*)" skillLevel=".*"/>.*""").match(sline)
        pprimary = compile(""".*<primaryAttribute>(.*)</primaryAttribute>.*""").match(sline)
        psecondary = compile(""".*<secondaryAttribute>(.*)</secondaryAttribute>.*""").match(sline)
        
        if pgroupname_groupid: # Happens only once
            info['groupname'] = pgroupname_groupid.groups()[0]
            info['groupid'] = int(pgroupname_groupid.groups()[1])
        if pname_groupid_id:
            info['name'] = pname_groupid_id.groups()[0]
            info['id'] = int(pname_groupid_id.groups()[1])
        if pdescription:
            info['description'] += pdescription.groups()[0]
        if prank:
            info['rank'] = int(prank.groups()[0])
        if prequired:
            info['required'].append(int(prequired.groups()[0]))
        if pprimary:
            info['primary'] = pprimary.groups()[0]
        if psecondary:
            info['secondary'] = psecondary.groups()[0]
        
        if info.has_key('secondary'): # Last object to be built
            #SKILLTREE[id] = Skill(id, 0, 0, name=name, rank=rank, primary=primary, secondary=secondary, groupname=groupname, groupid=groupid, description=description, dependencies=required)
            
            info['skilltable'] = TABLE_SKILL
            info['grouptable'] = TABLE_GROUP
            info['attributetable'] = TABLE_ATTRIBUTE
            
            db_conn.query("SELECT id FROM %(grouptable)s WHERE group_name = '%(groupname)s'" % info) # query for the groupname id
            groupid = db_conn.store_result()
            
            if groupid.num_rows() == 0:
                db_conn.query("INSERT INTO %(grouptable)s (group_name, group_id) VALUES ('%(groupname)s', '%(groupid)s')" % info) # query for the groupname id
                
                db_conn.query("SELECT id FROM %(grouptable)s WHERE group_name = '%(groupname)s'" % info) # query for the groupname id
                groupid = db_conn.store_result()
            
            # Finally
            info['groupname_id'] = int(groupid.fetch_row()[0][0]) # Grabs the single item
            
            db_conn.query("SELECT id FROM %(attributetable)s WHERE attribute_name = '%(primary)s'" % info) # query for the attribute id
            primaryid = db_conn.store_result()
            
            if primaryid.num_rows() == 0:
                db_conn.query("INSERT INTO %(attributetable)s (attribute_name) VALUES ('%(primary)s')" % info) # query for the groupname id
                
                db_conn.query("SELECT id FROM %(attributetable)s WHERE attribute_name = '%(primary)s'" % info) # query for the attribute id
                primaryid = db_conn.store_result()
            
            # Finally
            info['primary_id'] = int(primaryid.fetch_row()[0][0]) # Grabs the single item
            
            db_conn.query("SELECT id FROM %(attributetable)s WHERE attribute_name = '%(secondary)s'" % info) # query for the attribute id
            secondaryid = db_conn.store_result()
            
            if secondaryid.num_rows() == 0:
                db_conn.query("INSERT INTO %(attributetable)s (attribute_name) VALUES ('%(secondary)s')" % info) # query for the groupname id
                
                db_conn.query("SELECT id FROM %(attributetable)s WHERE attribute_name = '%(secondary)s'" % info) # query for the attribute id
                secondaryid = db_conn.store_result()
            
            # Finally
            info['secondary_id'] = int(secondaryid.fetch_row()[0][0]) # Grabs the single item
            
            # Replace the single quote with a double backslash and single quote
            info['description'] = info['description'].replace("'", "\\'")
            
            db_conn.query("INSERT INTO %(skilltable)s (skill_id, skill_name, rank, description, primary_attribute_id, secondary_attribute_id, groupname_id) VALUES (%(id)s, '%(name)s', %(rank)s, '%(description)s', %(primary_id)s, %(secondary_id)s, %(groupname_id)s)" % info) # commit skill
            
            # Hold the groupname and groupid [why?]
            groupname = info['groupname']
            groupid = info['groupid']
            # Reset everything
            info = {}
            info['groupname'] = groupname
            info['groupid'] = groupid
            info['description'] = ""
            info['required'] = []
            
    
    # TODO: Rewrite this for the database
    # Rebuild skill dependencies for each skill so that they are objects in a dictionary, for greater indexing
    #for skill in SKILLTREE:
    #    if SKILLTREE[skill]:
    #        requiredSkillsList = SKILLTREE[skill].dependencies
    #        SKILLTREE[skill].dependencies = {}
    #        for requiredSkill in requiredSkillsList:
    #            SKILLTREE[skill].dependencies[requiredSkill] = SKILLTREE[requiredSkill]

def getSkillInDatabase(columns=["skill_id","skill_name"], id="Null", name="Null"):
    '''
        Enter a single id and/or name and/or a list of ids and/or names
        example call: getSkillInDatabase(id=12099, name="Caldari Battleship)
        
        returns a list of tuples ordered (id, name)
    '''
    
    info = {}
    info['skilltable'] = TABLE_SKILL
    info['grouptable'] = TABLE_GROUP
    info['attributetable'] = TABLE_ATTRIBUTE
    info['skillname'] = name
    info['skillid'] = id
    query = "SELECT "
    
    if type(columns) == list and "*" not in columns:
        for column in columns:
            if column not in ["primary_attribute","secondary_attribute","groupname","primary_attribute_id","secondary_attribute_id","groupname_id"]:
                query += "%s" % column
                if column != columns[len(columns) - 1]:
                    query += ", "
    elif type(columns) == list and "*" in columns:
        # Error, you broke my heart :D
        return "ERROR: Query can not contain column names and an all delimiter at the same time"
    
    if columns == "*":
        columns = [("skill_id", "skill_name", "rank", "primary_attribute", "secondary_attribute", "groupname", "description")]
        
        # Full query
        query += "s.skill_id, s.skill_name, s.rank, a1.attribute_name primary_attribute, a2.attribute_name secondary_attribute, g.group_name group_name, s.description from %(skilltable)s s join %(attributetable)s a1 on s.primary_attribute_id = a1.id join %(attributetable)s a2 on s.secondary_attribute_id = a2.id join %(grouptable)s g on s.groupname_id = g.id" % info
    else:
        pa = False
        sa = False
        gn = False
        
        if "primary_attribute" in columns or "primary_attribute_id" in columns:
            ", a1.attribute_name primary_attribute"
        if "secondary_attribute" in columns or "secondary_attribute_id" in columns:
            ", a2.attribute_name secondary_attribute"
        if "groupname" in columns or "groupname_id" in columns:
            ", g.group_name group_name"
        
        query += " from %(skilltable)s" % info
        
        if pa:
            query += " join %(attributetable)s a1 on s.primary_attribute_id = a1.id" % info
        if sa:
            query += " join %(attributetable)s a2 on s.secondary_attribute_id = a2.id" % info
        if gn:
            query += " join %(grouptable)s g on s.groupname_id = g.id" % info
    
    if id != "Null" or name != "Null":
        query += " where "
        if type(info['skillname']) == list:
            for element in info['skillname']:
                query += "skill_name = '%s' " % element
                if element != info['skillname'][len(info['skillname'])-1]:
                    query += "or "
        elif info['skillname'] != 'Null':
            query += "skill_name = '%s' " % info['skillname']
        
        if type(info['skillid']) == list:
            if info['skillname']:
                query += "or "
            for element in info['skillid']:
                query += "skill_id = %s " % element
                if element != info['skillid'][len(info['skillid'])-1]:
                    query += "or "
        elif info['skillid']:
            if info['skillname'] != 'Null':
                query += "or skill_id = %s" % info['skillid']
            else:
                query += "skill_id = %s" % info['skillid']
    
    db_conn = MySQLdb.connection(user=DATABASE_USER, db=DATABASE_NAME, host=DATABASE_HOST)
    db_conn.query(query)
    
    returned = db_conn.store_result()
    
    requested = columns
    
    for row in range(returned.num_rows()):
        requested.append(returned.fetch_row()[0])
    
    return requested


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
    
    # Prebuild the characterobject
    characterobject = Character("Starting Up", characterID=-1, timeUpdated="Sometime Back")
    
    if DATABASE_PASSWORD != "":
        db_conn = MySQLdb.connection(user=DATABASE_USER, db=DATABASE_NAME, host=DATABASE_HOST, password=DATABASE_PASSWORD)
    else:
        db_conn = MySQLdb.connection(user=DATABASE_USER, db=DATABASE_NAME, host=DATABASE_HOST)
        
    db_conn.query("select s.skill_id, s.skill_name, s.rank, a1.attribute_name primary_attribute, a2.attribute_name secondary_attribute, g.group_name group_name, g.group_id, s.description from %(skilltable)s s join attribute a1 on s.primary_attribute_id = a1.id join %(attributetable)s a2 on s.secondary_attribute_id = a2.id join %(grouptable)s g on s.groupname_id = g.id order by s.groupname_id, s.rank" % {'skilltable': TABLE_SKILL, 'grouptable': TABLE_GROUP, 'attributetable': TABLE_ATTRIBUTE})
    
    skills = db_conn.store_result()
    
    for row in range(skills.num_rows()):
        skill = skills.fetch_row()[0]
        characterobject.addSkill(Skill(skill[0], 0, 0, name=skill[1], rank=skill[2], primary=skill[3], secondary=skill[4], groupname=skill[5], groupid=skill[6], description=skill[7]))
    
    
    for line in characterSheet.readlines():
        if compile(""".*<currentTime>(.*)</currentTime>.*""").match(line):
            timeUpdated = compile(""".*<currentTime>(.*)</currentTime>.*""").match(line).groups()[0]
        
        if compile(""".*<characterID>(.*)</characterID>.*""").match(line):
            characterID = compile(""".*<characterID>(.*)</characterID>.*""").match(line).groups()[0]
        
        if compile(""".*<name>(.*)</name>.*""").match(line):
            characterobject.name = compile(""".*<name>(.*)</name>.*""").match(line).groups()[0]
            characterobject.characterID = characterID
            characterobject.timeUpdated = timeUpdated
            
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
            
            if id in characterobject.skillset:
                characterobject.editSkill(id, skillpoints=skillpoints, level=level) # If the skill exists, update it
            else:
                characterobject.addSkill(Skill(id, skillpoints, level)) # if not, build it out
        
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
    
    # Read in this information while the rest is being built
    class Threading(threading.Thread):
        def __init__(self, function, cObject, params):
            threading.Thread.__init__(self)
            self.function = function
            self.cObject = cObject
            self.params = params
        
        def run(self):
            self.function(self.cObject, self.params)
            self._Thread__stop()
    
    timeUpdated = None
    characterID = None
    augmentorName = None
    characterobject = None
    slot = 1

    characterobject = Character("Starting Up", characterID=-1, timeUpdated="Sometime Back")
    
    db_conn = MySQLdb.connection(user=DATABASE_USER, db=DATABASE_NAME, host=DATABASE_HOST, passwd=DATABASE_PASSWORD)
    db_conn.query("select s.skill_id, s.skill_name, s.rank, a1.attribute_name primary_attribute, a2.attribute_name secondary_attribute, g.group_name group_name, g.group_id, s.description from %(skilltable)s s join attribute a1 on s.primary_attribute_id = a1.id join %(attributetable)s a2 on s.secondary_attribute_id = a2.id join %(grouptable)s g on s.groupname_id = g.id order by s.groupname_id, s.rank" % {'skilltable': TABLE_SKILL, 'grouptable': TABLE_GROUP, 'attributetable': TABLE_ATTRIBUTE})
    
    skills = db_conn.store_result()
    
    for row in range(skills.num_rows()):
        skill = skills.fetch_row()[0]
        characterobject.addSkill(Skill(skill[0], 0, 0, name=skill[1], rank=skill[2], primary=skill[3], secondary=skill[4], groupname=skill[5], groupid=skill[6], description=skill[7]))
    
    charactersheet = apiSelect("charactersheet", params)
    
    data = charactersheet.read()
    
    for line in data.split("\r\n"):
        if compile(""".*<currentTime>(.*)</currentTime>.*""").match(line):
            timeUpdated = compile(""".*<currentTime>(.*)</currentTime>.*""").match(line).groups()[0]
        
        if compile(""".*<characterID>(.*)</characterID>.*""").match(line):
            characterID = compile(""".*<characterID>(.*)</characterID>.*""").match(line).groups()[0]
        
        if compile(""".*<name>(.*)</name>.*""").match(line):
            characterobject.name = compile(""".*<name>(.*)</name>.*""").match(line).groups()[0]
            characterobject.characterID = characterID
            characterobject.timeUpdated = timeUpdated
            
            buildingSkills = Threading(gatherAllBasicSkills, characterobject, params)
            buildingSkills.start()
        
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
            while not characterobject.ready:
                continue # wait on all the skills to be assigned
            
            skillInfo = compile(""".*<row typeID="(.*)" skillpoints="(.*)" level="(.*)" />.*""").match(line).groups()
            id = int(skillInfo[0])
            skillpoints = int(skillInfo[1])
            level = int(skillInfo[2])
            
            if id in characterobject.skillset:
                characterobject.editSkill(id, skillpoints=skillpoints, level=level) # If the skill exists, update it
            else:
                characterobject.addSkill(Skill(id, skillpoints, level)) # if not, build it out
        
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
        
    assigning = Threading(assignCurrentlyTraining, characterobject, params)
    assigning.start()
    
    return characterobject

def gatherAllBasicSkills(cObject, *args, **kws):
    '''
        Grabs all the skills from the database and assigns them to self
    '''
    db_response = getSkillInDatabase("*")
    db_response = db_response[1:]
    
    for row in db_response:
        cObject.addSkill(Skill(id=int(row[0]), skillpoints=0, level=0, name=row[1], rank=int(row[2]), primary=row[3], secondary=row[4], groupname=row[5], groupid=-1, description=row[6]))
        cObject.ready = True

def assignCurrentlyTraining(cObject, params):
    '''
        Adjusts the currently training skill to 
    '''

    response = apiSelect("skillintraining", params)
    
    response = response.read()
    
    skillintraining = None
    
    for line in response.split("\r\n"):
        if compile(""".*<skillInTraining>(.*)</skillInTraining>.*""").match(line):
            skillintraining = int(compile(""".*<skillInTraining>(.*)</skillInTraining>.*""").match(line).groups()[0])
            print skillintraining
        
        if compile(""".*<trainingEndTime>(.*)</trainingEndTime>.*""").match(line):
            endtime = compile(""".*<trainingEndTime>(.*)</trainingEndTime>.*""").match(line).groups()[0]
        
        if compile(""".*<trainingStartTime>(.*)</trainingStartTime>.*""").match(line):
            starttime = compile(""".*<trainingStartTime>(.*)</trainingStartTime>.*""").match(line).groups()[0]
        
        if compile(""".*<trainingTypeID>(.*)</trainingTypeID>.*""").match(line):
            skillid = int(compile(""".*<trainingTypeID>(.*)</trainingTypeID>.*""").match(line).groups()[0])
        
        if skillintraining == 0:
            cObject.setCurrentlyTraining(Skill(-1, 0, 0, name="Nothing Training"))
        elif skillintraining == 1:
            while not cObject.ready:
                continue # Wait on all the skills to finish parsing
            skill = getSkillInDatabase("*", id=skillid)[1]
            time.sleep(3)
            cSkill = Skill(id=skill[0], skillpoints=cObject.getSkill(skill[0]).skillpoints, level=cObject.getSkill(skill[0]).level, name=skill[1], rank=skill[2], primary=skill[3], secondary=skill[4], groupname=skill[5], description=skill[6])
            # Special attributes for the currently trainning skill
            cSkill.__setattr__("trainingLevel", (cSkill.level + 1))
            cSkill.__setattr__("finishing", endtime)
            cSkill.__setattr__("started", starttime)
            cObject.setCurrentlyTraining(cSkill)


def apiSelect(item, params):
    '''Options:
        \tWalletTransactions    : requires full API key
        \tCharacterSheet        : Returns the current character sheet
        \tSkillInTraining       : Returns the current skill trainning, 0 for no skill
        \tSkillTree             : Returns the entire skill tree for EVE
        \tRefTypes              : Returns the reference types for the wallet
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
    else:
        return "Error: Not a selection in the list"
    
    response = conn.getresponse()

    conn.close
    
    return response


# ONLY UPDATE WITH THIS COMMAND FOR NEW DATABASES!!
#_buildSkillTree({
#    'characterID': 672389577, # Lucitania
#    'userid': 1690689,
#    'apikey': 'jdFQPL18o0TvoZ63KnQeVGE1kw8KQ7iJDFYNjhxc0RMLLpfgRAz5nod5MiuJElCB' # Public
#    }) # Arbitray information for the pull

