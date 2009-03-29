#!/usr/bin/python

import wx

ID_PLUS = 10
ID_MINUS = 11

class LeftPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        
        # Pulls the right panel from the parent and edits its text, assumes this location
        self.text = parent.GetParent().rightPanel.text

        button1 = wx.Button(self, ID_PLUS, '+', (10, 10))
        button2 = wx.Button(self, ID_MINUS, '-', (10, 60))
        
        # Binds the events of pressing each button to their functions
        #self.Bind(wx.EVT_BUTTON, self.OnPlus, id=button1.GetId())
        #self.Bind(wx.EVT_BUTTON, self.OnMinus, id=button2.GetId())
        
        self.Bind(wx.EVT_BUTTON, self.OnPlus, id=ID_PLUS)
        self.Bind(wx.EVT_BUTTON, self.OnMinus, id=ID_MINUS)

    def OnPlus(self, event):
        value = int(self.text.GetLabel())
        value = value + 1
        self.text.SetLabel(str(value))

    def OnMinus(self, event):
        value = int(self.text.GetLabel())
        value = value - 1
        self.text.SetLabel(str(value))


class RightPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        
        # Text that will be displayed
        self.text = wx.StaticText(self, -1, '0', (40, 60))


class Communicate(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(280, 200))

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
        self.Show(True)

app = wx.App()
Communicate(None, -1, 'Widgets Communicate')
app.MainLoop()
