from EVECharacter import *

lucitania = extractXML("Lucitania.xml")
xressmeth = extractXML("Xressmeth.xml")

params = {
    'characterID': 672389577,
    'userid': 1690689,
    #'apikey': 'jdFQPL18o0TvoZ63KnQeVGE1kw8KQ7iJDFYNjhxc0RMLLpfgRAz5nod5MiuJElCB'
    'apikey': 'C35335BEE7054E13AC80AD63E7AE2FB1FD5430420671448E88AD279FCFC4BF0B'
    }

buildSkillTree(params)

api = extractAPI(params)


