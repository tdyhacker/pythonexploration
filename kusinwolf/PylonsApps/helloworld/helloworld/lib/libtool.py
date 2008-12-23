from re import compile


#from helloworld.model.meta import *
#from helloworld.model.tags_table import *
#from helloworld.model.link_table import *
#
#tags=['bibliography', 'casual', 'color', 'colorwheel', 'div', 'economics', 'engine', 'experiement', 'facepunch', 'fleetbattles', 'forums', 'from', 'game', 'garrysmod', 'generator', 'gmail', 'gmod', 'google', 'hex', 'mail', 'mmo', 'music', 'old;', 'online', 'pandora', 'radio', 're', 'reference', 'regularexpression', 'resource', 'rpg', 'science', 'search', 'select', 'ships', 'sifi', 'space', 'sqlite', 'stragey', 'tags', 'tool', 'travian', 'tutorial', 'wiki', 'wow']
#for tag in tags:
#    meta.Session.save(Tag(tag))
#meta.Session.commit()

# Evil List comprension that performs 3 querys in a single line while gathering all the tags for the selected link
#tags = [meta.Session.query(Tag).filter_by(id=xref.tag_id).first() for xref in meta.Session.query(Link_xref_tag).filter_by(link_id=meta.Session.query(Links).first().id).all()]


def linkAppend(name):
    if not compile("http://(.*)").match(name):
        name = "http://%s" % name
    if not compile("(.*).com(.*)").match(name):
        name = "%s.com/" % name
    if compile("http://.*/(.*)").match(name):
        name = "http://%s%s" % (compile("http://(.*)(/.*)").match(name).groups()[0], compile("http://(.*)(/.*)").match(name).groups()[1])
        if compile("http://(.*)(/.*)").match(name).groups()[1] == '':
            name = "%s/" % name
    return name

def isInTable(sSession, sClass, sInfo):
    "send -> Session object, Class object, Column name object, & compare object -> Returns boolean"
    if sSession.query(sClass).select_whereclause(sInfo):
        return True
    else:
        return False