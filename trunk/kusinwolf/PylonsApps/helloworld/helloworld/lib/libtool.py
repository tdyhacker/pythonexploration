from re import compile

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