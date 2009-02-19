from EVECharacter import *

# Offline method of parsing information
#lucitania = extractXML("Lucitania.xml")
#xressmeth = extractXML("Xressmeth.xml")

lucitania = extractAPI({
    'characterID': 672389577, # Lucitania
    'userid': 1690689,
    'apikey': 'jdFQPL18o0TvoZ63KnQeVGE1kw8KQ7iJDFYNjhxc0RMLLpfgRAz5nod5MiuJElCB' # Public
    })

xressmeth = extractAPI({
    'characterID': 160054538, # Xress Meth
    'userid': 1776244,
    'apikey': 'd326ybm33XBUXNuek2chNTTqV9yyyu2SAAoZSax3srYk1EU4y7ziobOjjOX247LQ' # Public
    })

# Main Application
app = wx.App()
# Builds a Window
Browser(None, -1, 'Character Browser', xressmeth)
# Builds another Window
Browser(None, -1, 'Character Browser', lucitania)
app.MainLoop() # starts the entire application


