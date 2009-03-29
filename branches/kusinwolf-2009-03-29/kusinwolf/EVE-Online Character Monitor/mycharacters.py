from EVEDatabase import DatabaseControl
from EVEGUI import Browser
import wx

lucitania_controller = DatabaseControl(
    characterID=672389577, # Lucitania
    userid=1690689,
    apikey='jdFQPL18o0TvoZ63KnQeVGE1kw8KQ7iJDFYNjhxc0RMLLpfgRAz5nod5MiuJElCB' # Public
    )
lucitania = lucitania_controller.extract()
##lucitania = lucitania_controller.extract("Lucitania.xml")
#
#xressmeth_controller = DatabaseControl(
#    characterID=160054538, # Xress Meth
#    userid=1776244,
#    apikey='d326ybm33XBUXNuek2chNTTqV9yyyu2SAAoZSax3srYk1EU4y7ziobOjjOX247LQ' # Public
#    )
#
#xressmeth = xressmeth_controller.extract()
##xressmeth = xressmeth_controller.extract("Xressmeth.xml")

#test_controller = DatabaseControl()
#test = test_controller.extract(DEBUG=True)

# Main Application
#app = wx.App()
## Builds a Window
#Browser(None, -1, 'Character Browser', xressmeth)
## Builds another Window
#Browser(None, -1, 'Character Browser', lucitania)
#Browser(None, -1, 'Character Browser', test)
#app.MainLoop() # starts the entire application