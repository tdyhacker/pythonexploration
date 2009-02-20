import wx
import MySQLdb # Will need soon once full functionality comes about
from EVECharacter import Skill, Character, Certificate, Augmentation, Title
from EVEDatabase import extractAPI


###################
# wxPython Window #
###################

# Tutorial
#http://zetcode.com/wxpython/

ID_QUIT = 1
ID_LEVEL0 = 100
ID_LEVEL1 = 101
ID_LEVEL2 = 102
ID_LEVEL3 = 103
ID_LEVEL4 = 104
ID_LEVEL5 = 105

class BottomPanel(wx.Panel):
    def __init__(self, parent, id, cObject):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        
        self.cObject = cObject # Character Object
        
        skillNamePanel = wx.Panel(self, -1, (5, 64))
        skillPointsPanel = wx.Panel(self, -1)
        rankPanel = wx.Panel(self, -1)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        # Add(item, proportion percentage, flags, border size)
        hbox.Add(skillNamePanel, 10, wx.EXPAND | wx.ALL, 5)
        hbox.Add(skillPointsPanel, 3, wx.EXPAND | wx.ALL, 5)
        hbox.Add(rankPanel, 2, wx.EXPAND | wx.ALL, 5)
        
        self.skillname = wx.StaticText(skillNamePanel, -1, 'Skill', (0, 0))
        self.skillpoints = wx.StaticText(skillPointsPanel, -1, '0', (0, 0))
        self.rank = wx.StaticText(rankPanel, -1, '0x', (0, 0))
        
        self.SetSizer(hbox)
    
    def DisplayLevel(self, level):
        skillnamelist = "SkillName at Level %s\n" % level
        skillpointslist = "SkillPoints\n"
        ranklist = "Rank\n"
        
        for skill in self.cObject.__getattribute__("level%s" % level):
            skillnamelist += str(skill.name) + "\n"
            skillpointslist += str(skill.skillpoints) + "\n"
            ranklist += str(skill.rank) + "x\n"

        self.skillname.SetLabel(skillnamelist)
        self.skillpoints.SetLabel(skillpointslist)
        self.rank.SetLabel(ranklist)

class Browser(wx.Frame):
    def __init__(self, parent, id, title, cObject, size=(500, 1024)):
        self.cObject = cObject # ChacterObject passed in
        # The entire window
        wx.Frame.__init__(self, parent, id, title, size) # Width, Height
        # A chunk of the GUI inside the frame
        panel = wx.Panel(self, -1)
        
        self.bottompanel = BottomPanel(panel, -1, cObject)
        
        # Menu information
        menubar = wx.MenuBar() # Creates the full menu bar
        file = wx.Menu() # Creates the file menu
        
        # Builds quit MenuItem in AppendItem
        file.AppendItem(wx.MenuItem(file, ID_QUIT, '&Quit\tCtrl+Q')) # Appends Quit option to File menu
        
        menubar.Append(file, '&File') # Adds File Menu to the full menu bar
        self.SetMenuBar(menubar) # Builds the menubar
        
        # Binds a user generated event to the OnQuit method
        self.Bind(wx.EVT_MENU, self.OnQuit, id=1)
        
        # Grabbing font
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        
        # Building mutable inner box, like a div or table
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Build row inside mutable box
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Creates static text
        stext = wx.StaticText(panel, -1, 'Character Name:')
        stext.SetFont(font)
        
        # adds it to the horizontal box
        hbox1.Add(stext, 0, wx.RIGHT, 8)
        
        # Creates static text
        stext = wx.StaticText(panel, -1, self.cObject.name)
        stext.SetFont(font)
        
        # adds it to the horizontal box
        hbox1.Add(stext, 1)
        vbox.Add(hbox1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        
        # Spacer
        vbox.Add((-1,10))
        
        # Creating buttons
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        
        btn = wx.Button(panel, ID_LEVEL0, 'Level 0', size=(70, 30))
        hbox5.Add(btn, 0)
        
        btn = wx.Button(panel, ID_LEVEL1, 'level 1', size=(70, 30))
        hbox5.Add(btn, 0, wx.LEFT, 5)
        
        btn = wx.Button(panel, ID_LEVEL2, 'Level 2', size=(70, 30))
        hbox5.Add(btn, 0, wx.LEFT, 5)
        
        btn = wx.Button(panel, ID_LEVEL3, 'Level 3', size=(70, 30))
        hbox5.Add(btn, 0, wx.LEFT, 5)
        
        btn = wx.Button(panel, ID_LEVEL4, 'Level 4', size=(70, 30))
        hbox5.Add(btn, 0, wx.LEFT, 5)
        
        btn = wx.Button(panel, ID_LEVEL5, 'Level 5', size=(70, 30))
        hbox5.Add(btn, 0, wx.LEFT, 5)
        
        vbox.Add(hbox5, 0, wx.ALIGN_CENTER | wx.CENTER, 10)
        
        # Binds a user generated event to the OnQuit method
        self.Bind(wx.EVT_BUTTON, self.OnLevel0, id=ID_LEVEL0)
        self.Bind(wx.EVT_BUTTON, self.OnLevel1, id=ID_LEVEL1)
        self.Bind(wx.EVT_BUTTON, self.OnLevel2, id=ID_LEVEL2)
        self.Bind(wx.EVT_BUTTON, self.OnLevel3, id=ID_LEVEL3)
        self.Bind(wx.EVT_BUTTON, self.OnLevel4, id=ID_LEVEL4)
        self.Bind(wx.EVT_BUTTON, self.OnLevel5, id=ID_LEVEL5)
        
        # Spacer
        vbox.Add((-1,10))
        
        vbox.Add(self.bottompanel, 1, wx.EXPAND | wx.ALL, 5)
        
        # Sets the sizer object
        panel.SetSizer(vbox)

        # Centers on the screen
        self.Centre()
        
        self.SetSize(size) # Adjust size after the Sizer has been built
        
        # Keeps the window visable to the human
        self.Show(True)
        
        #panel.SetSize((400,400)) Is this even used?
    
    def OnLevel0(self, event):
        self.bottompanel.DisplayLevel(0)
    
    def OnLevel1(self, event):
        self.bottompanel.DisplayLevel(1)
    
    def OnLevel2(self, event):
        self.bottompanel.DisplayLevel(2)
    
    def OnLevel3(self, event):
        self.bottompanel.DisplayLevel(3)
    
    def OnLevel4(self, event):
        self.bottompanel.DisplayLevel(4)

    def OnLevel5(self, event):
        self.bottompanel.DisplayLevel(5)
    
    def OnQuit(self, event):
        self.Close()