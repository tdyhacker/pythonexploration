from globals import *
from classes import *

############################
# Left Pannel With Buttons #
############################

class LeftButtonPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        self.parent = parent
        
        # GUI Buttons that the user can click on
        wx.Button(self, 1, 'Square', pos = (0, 10), size = (-1, 25))
        wx.Button(self, 2, 'Triangle', pos = (0, 50), size = (-1, 25))
        wx.Button(self, 3, 'Link', pos = (0, 90), size = (-1, 25))
        
        # Binds for button events
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=1)
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=2)
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=3)