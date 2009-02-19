from EVECharacter import *
import wx

lucitania = extractXML("Lucitania.xml")
#xressmeth = extractXML("Xressmeth.xml")

#params = {
#    'characterID': 672389577,
#    'userid': 1690689,
#    #'apikey': 'jdFQPL18o0TvoZ63KnQeVGE1kw8KQ7iJDFYNjhxc0RMLLpfgRAz5nod5MiuJElCB' # Partical
#    'apikey': 'C35335BEE7054E13AC80AD63E7AE2FB1FD5430420671448E88AD279FCFC4BF0B' # Full
#    }
#
#api = extractAPI(params)

# Tutorial
#http://zetcode.com/wxpython/

ID_QUIT = 1

ID_LEVEL1 = 100
ID_LEVEL2 = 101
ID_LEVEL3 = 102
ID_LEVEL4 = 103
ID_LEVEL5 = 104

class Browser(wx.Frame):
    def __init__(self, parent, id, title, cObject, size=(1024, 768)):
        self.cObject = cObject # ChacterObject passed in
        # The entire window
        wx.Frame.__init__(self, parent, id, title, size) # Width, Height
        # A chunk of the GUI inside the frame
        panel = wx.Panel(self, -1)
        
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
        
        btn = wx.Button(panel, ID_LEVEL1, 'Level 1', size=(70, 30))
        hbox5.Add(btn, 0)
        
        btn = wx.Button(panel, ID_LEVEL2, 'Level 2', size=(70, 30))
        hbox5.Add(btn, 0, wx.LEFT , 5)
        
        btn = wx.Button(panel, ID_LEVEL3, 'Level 3', size=(70, 30))
        hbox5.Add(btn, 0, wx.LEFT, 5)
        
        btn = wx.Button(panel, ID_LEVEL4, 'Level 4', size=(70, 30))
        hbox5.Add(btn, 0, wx.LEFT, 5)
        
        btn = wx.Button(panel, ID_LEVEL5, 'Level 5', size=(70, 30))
        hbox5.Add(btn, 0, wx.LEFT, 5)
        
        vbox.Add(hbox5, 0, wx.ALIGN_CENTER | wx.CENTER, 10)
        
        # Binds a user generated event to the OnQuit method
        self.Bind(wx.EVT_BUTTON, self.OnLevel1, id=ID_LEVEL1)
        self.Bind(wx.EVT_BUTTON, self.OnLevel2, id=ID_LEVEL2)
        self.Bind(wx.EVT_BUTTON, self.OnLevel3, id=ID_LEVEL3)
        self.Bind(wx.EVT_BUTTON, self.OnLevel4, id=ID_LEVEL4)
        self.Bind(wx.EVT_BUTTON, self.OnLevel5, id=ID_LEVEL5)

        
        # Spacer
        vbox.Add((-1,10))
        
        # Sets the sizer object
        panel.SetSizer(vbox)
        
        # Centers on the screen
        self.Centre()
        
        # Keeps the window visable to the human
        self.Show(True)
    
    def OnLevel1(self, event):
        # Spawn child
        app = wx.App()
        Browser(self, -1, 'Level 1' % event, lucitania, size=(350,200))
        app.MainLoop()
    
    def OnLevel2(self, event):
        # Spawn child
        app = wx.App()
        Browser(self, -1, 'Level 2' % event, lucitania, size=(350,200))
        app.MainLoop()
    
    def OnLevel3(self, event):
        # Spawn child
        app = wx.App()
        Browser(self, -1, 'Level 3' % event, lucitania, size=(350,200))
        app.MainLoop()
    
    def OnLevel4(self, event):
        # Spawn child
        app = wx.App()
        Browser(self, -1, 'Level 4' % event, lucitania, size=(350,200))
        app.MainLoop()

    def OnLevel5(self, event):
        # Spawn child
        app = wx.App()
        Browser(self, -1, 'Level 5' % event, lucitania, size=(350,200))
        app.MainLoop()
    
    def OnQuit(self, event):
        self.Close()


app = wx.App()
Browser(None, -1, 'Character Browser', lucitania)
app.MainLoop()


