from re import compile

from helloworld.model import meta
from helloworld.model.link_table import *
from helloworld.model.tags_table import *

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

def buildTags(link, tags):
    '''Pass in the saved link object to have its tags evaluated'''
    for tag in compile('(\S\w*)').findall(tags):
        if not meta.Session.query(Tag).filter_by(tag=tag).first():
            meta.Session.save(Tag(tag))
            meta.Session.commit()
        meta.Session.save(Link_xref_tag(link.getID(), meta.Session.query(Tag).filter_by(tag=tag).first().id))
        meta.Session.commit()
        