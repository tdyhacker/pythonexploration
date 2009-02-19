#!/usr/bin/python

import wx

class Size(wx.Frame):
    def __init__(self, parent, id, title,
                 size=(250, 200), move=(200, 200), center=False):
        
        wx.Frame.__init__(self, parent,
                          id, title, size=size) # size=(width, height)
        
        if not center:
            # Moves the window to a designated location
            self.Move(move)
        else:
            # Moves the window to the center of the screen
            self.Centre()
        
        self.Show(True)


app = wx.App()
Size(None, -1, 'Size 250x200') # Default size
Size(None, -2, 'Size 800x600', size=(800, 600)) # New Size

Size(None, -1, 'Move 200x200') # Default move
Size(None, -2, 'Move 800x600', move=(800, 600)) # New Move

Size(None, -2, 'Center', center=True) # Center
app.MainLoop()

