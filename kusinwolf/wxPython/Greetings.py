#!/usr/bin/python

import wx
import random

ID_PLUS = 10
ID_MINUS = 11
ID_RANDOM = 12

class LeftPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        
        # Pulls the right panel from the parent and edits its text, assumes this location
        self.rightPanel = parent.GetParent().rightPanel
        self.text = parent.GetParent().rightPanel.text

        button1 = wx.Button(self, ID_PLUS, '+', (10, 10))
        button2 = wx.Button(self, ID_MINUS, '-', (10, 60))
        #button2 = wx.Button(self, ID_RANDOM, 'Random', (10, 110))
        
        self.Bind(wx.EVT_BUTTON, self.OnPlus, id=ID_PLUS)
        self.Bind(wx.EVT_BUTTON, self.OnMinus, id=ID_MINUS)
        #self.Bind(wx.EVT_BUTTON, self.OnRandom, id=ID_RANDOM)

    def OnPlus(self, event):
        # resetting the text to be the new selection
        self.text.SetLabel(self.rightPanel.next())

    def OnMinus(self, event):
        # resetting the text to be the new selection
        self.text.SetLabel(self.rightPanel.prev())

    #def OnRandom(self, event):
    #    # resetting the text to be the new selection
    #    self.text.SetLabel(self.rightPanel.random())


class RightPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        self.textlist = ["Hello!", "Howdy!", "How's it going?", "What's up?", "Sup?"]
        self.textpos = 0
        
        # Text that will be displayed
        self.text = wx.StaticText(self, -1, self.textlist[0], (40, 60))
    
    def next(self):
        if self.textpos >= len(self.textlist) - 1:
            self.textpos = 0
        else:
            self.textpos += 1
            
        return self.textlist[self.textpos]
    
    def prev(self):
        if self.textpos <= 0:
            self.textpos = len(self.textlist) - 1
        else:
            self.textpos -= 1
            
        return self.textlist[self.textpos]

    #def random(self):
    #    return self.textlist[int(random.Random().random() * len(self.textlist))]


class Communicate(wx.Frame):
    def __init__(self, parent, id, title, size=(400, 200)):
        wx.Frame.__init__(self, parent, id, title, size=size)

        panel = wx.Panel(self, -1)
        
        # Builds Right Panel from class
        self.rightPanel = RightPanel(panel, -1)
        
        # Builds Left Panel from class
        leftPanel = LeftPanel(panel, -1)
        
        # builds a box to add panels
        hbox = wx.BoxSizer()
        
        # Addes both left and right panels
        hbox.Add(leftPanel, 1, wx.EXPAND | wx.ALL, 5)
        hbox.Add(self.rightPanel, 1, wx.EXPAND | wx.ALL, 5)
        
        # Sets the main panel to the generated box
        panel.SetSizer(hbox)
        
        self.Centre()
        self.SetSize(size) # Adjust size after the Sizer has been built
        self.Show(True)

app = wx.App()
Communicate(None, -1, 'Greetings')
app.MainLoop()
