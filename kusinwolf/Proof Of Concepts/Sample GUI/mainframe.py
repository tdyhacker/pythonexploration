# Pieces of GUI program
from globals import *
from classes import *
from rightpanel import *
from leftpanel import *
from canvas import *
import os
from re import compile


# http://www.zetcode.com/wxpython/ - great guide out there
# http://wiki.wxpython.org/AnotherTutorial - Another great guide
# http://wiki.wxpython.org/Getting%20Started - Another useful resource
# http://wiki.wxpython.org/DoubleBufferedDrawing - Best explination about buffering and reducing flicker in graphics
# http://wiki.wxpython.org/wxOGL

#################################
# Main Frame wraping everything #
#################################

class MainFrame(wx.Frame):
    def __init__(self, parent, id, title, size = (1024, 768) ):
        wx.Frame.__init__(self, parent, id, title, pos = (0,0), size = size)
        
        self.FileSavingTo = None
        self.Path = None
        self.Filename = None
        self.ViewType = 1 # Simple Mode by default
        self.FlippedGroups = False
        
        self.CurrentGroups = []
        self.Variables = []
        
        # Parts of the entire Frame
        self.Canvas = Canvas(self, 1)
        self.LeftButtonPanel = LeftButtonPanel(self, 2)
        self.RightPanel = RightPanel(self, 3)
        
        # Attempt at building tabs
        nb = wx.Notebook(self.RightPanel)
        
        # NoteBook Pages
        page1 = Page1(nb)
        page2 = Page2(nb)
        page3 = Page3(nb)
        
        nb.AddPage(page1, "Node")
        self.RightPanel.AddTab(page1)
        nb.AddPage(page2, "Vars")
        self.RightPanel.AddTab(page2)
        nb.AddPage(page3, "Overview")
        self.RightPanel.AddTab(page3)
        
        # Build out space for the notebook
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        self.RightPanel.SetSizer(sizer)
        
        # File menu.
        filemenu = wx.Menu()
        filemenu.Append(MENU_ID_NEW, "&New","New canvas and file")
        filemenu.Append(MENU_ID_LOAD, "&Open","Load existing canvas")
        filemenu.AppendSeparator()
        filemenu.Append(MENU_ID_SAVE, "&Save","Save current canvas")
        filemenu.Append(MENU_ID_SAVEAS, "Save &As...","Save current canvas to a new file")
        filemenu.Append(MENU_ID_SAVE_IMAGE, "Save &Image","Print the current canvas to picture form")
        filemenu.AppendSeparator()
        filemenu.Append(MENU_ID_EXIT,"E&xit","Terminate the program")
        
        # Edit Menu
        edit = wx.Menu()
        edit.Append(MENU_COPY_INTERACTABLE, "&Copy", "Copy the selected item")
        edit.Append(MENU_PASTE_INTERACTABLE, "&Paste", "Paste the selected item")
        edit.Append(MENU_DELETE_INTERACTABLE, "&Delete", "Delete the selected item")
        
        # Canvas Menu
        canvas = wx.Menu()
        canvas.Append(MENU_ID_CLEAR_CANVAS, "&Clear Canvas", "Removes everything on the canvas")
        
        # Help Menu
        helpmenu = wx.Menu()
        helpmenu.Append(MENU_ID_ABOUT, "&About"," Information about this program")
        helpmenu.Append(MENU_DEBUG_MODE, "&Debug","Debugging")
        
        # View Menu
        viewmenu = wx.Menu()
        viewmenu.Append(MENU_ID_FLIP_GROUPS, "&Flip Groups", "Convert groups from vertical to horizontal and vice versa")
        viewmenu.AppendSeparator()
        viewmenu.Append(MENU_ID_SORT_LINEAR, "&Linear Sort", "Sort out the interactables in linear order based on transition")
        #viewmenu.Append(MENU_ID_ADVANCEDVIEW, "&Advanced Mode")
        #viewmenu.Append(MENU_ID_SIMPLEVIEW, "&Simple Mode")
        
        # Build and add the entire menu bar to the window
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(edit, "&Edit")
        menuBar.Append(viewmenu, "&View")
        menuBar.Append(canvas, "&Canvas")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)

        # Bind menu events to methods
        wx.EVT_MENU(self, MENU_ID_ADVANCEDVIEW, self.OnViewAdvanced)
        wx.EVT_MENU(self, MENU_ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, MENU_ID_CLEAR_CANVAS, self.OnClearCanvas)
        wx.EVT_MENU(self, MENU_ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, MENU_ID_FLIP_GROUPS, self.OnFlipGroups)
        wx.EVT_MENU(self, MENU_ID_LOAD, self.OnLoad)
        wx.EVT_MENU(self, MENU_ID_NEW, self.OnNew)
        wx.EVT_MENU(self, MENU_ID_SAVE, self.OnSave)
        wx.EVT_MENU(self, MENU_ID_SAVEAS, self.OnSaveAs)
        wx.EVT_MENU(self, MENU_ID_SAVE_IMAGE, self.OnSaveImage)
        wx.EVT_MENU(self, MENU_ID_SIMPLEVIEW, self.OnViewSimple)
        wx.EVT_MENU(self, MENU_ID_SORT_LINEAR, self.OnSortLinear)
        
        wx.EVT_MENU(self, MENU_DEBUG_MODE, self.Debug)
        
        wx.EVT_MENU(self, MENU_COPY_INTERACTABLE, self.OnCopy)
        wx.EVT_MENU(self, MENU_PASTE_INTERACTABLE, self.OnPaste)
        wx.EVT_MENU(self, MENU_DELETE_INTERACTABLE, self.OnDelete)
        
        # Create base layer of the window to assign a size to
        self.layoutSizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.layoutSizer.Add(self.ButtonSizer, 1, wx.EXPAND)
        
        self.layoutSizer.Add(self.LeftButtonPanel, 0, wx.VERTICAL)
        self.layoutSizer.Add(self.Canvas, 4, wx.VERTICAL | wx.HORIZONTAL | wx.EXPAND)
        self.layoutSizer.Add(self.RightPanel, 0, wx.RIGHT | wx.VERTICAL | wx.EXPAND)
        
        self.layoutSizer.GetSizeTuple()
        
        # Assign the base layer to the window
        self.SetSizer(self.layoutSizer)
        self.SetAutoLayout(1)
        # Using this resets the size of the window which is not what I want right now
        #self.layoutSizer.Fit(self)
        # Simplifies setting Sizer, Setting Auto Layout and fitting the window to the sizer
        
        #self.SetSizerAndFit(self.layoutSizer)
        
        self.Centre()
        self.Show(True)
    
    def Debug(self):
        pass
    
    def AddVariable(self, nvar):
        found = False
        
        for ovar in self.GetVariables():
            if nvar.lower() == ovar.lower():
                found = True
        
        if not found and nvar.lower() != '':
            self.Variables.append(nvar)
            self.Variables.sort()
    
    def GetFlippedGroups(self):
        return self.FlippedGroups
    
    def GetLastClickedOn(self):
        return self.Canvas.GetLastClickedOn()
    
    def GetGroups(self):
        return self.CurrentGroups
    
    def GetVariables(self):
        return self.Variables
    
    def InViewAdvanced(self):
        return self.ViewType == 2
    
    def InViewSimple(self):
        return self.ViewType == 1
    
    def LoadFile(self):
        pass
    
    def OnCopy(self, event):
        self.Canvas.OnCopy(event)
    
    def OnPaste(self, event):
        self.Canvas.OnPaste(event)
    
    def OnDelete(self, event):
        self.Canvas.OnDelete(event)
    
    def OnAbout(self, event):
        dialog = wx.MessageDialog(self, "This is only a prototype for designing a GUI", "Prototype Help", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    
    def OnClearCanvas(self, event):
        self.Canvas.ClearCanvas()
    
    def OnExit(self, event):
        # Clear the memory to prevent ipython from causing problems
        del self.Canvas
        del self.FileSavingTo
        del self.layoutSizer
        del self.LeftButtonPanel
        del self.RightPanel
        self.Close(True)
    
    def OnFlipGroups(self, event):
        self.FlippedGroups = self.FlippedGroups ^ True # Xor (flip-flop)
        
        self.Canvas.DoDrawing()

    def OnLoad(self, event):
        dlg = wx.FileDialog(self, "Open a file", style=wx.FD_OPEN)
        
        wildcard =  "TXT files (.txt)|*.txt|" \
                    "All files (*.*)|*.*"
        dlg.SetWildcard(wildcard)
        
        dlg.Raise() # This brings the window up for the user to interact with
        
        if dlg.ShowModal() == wx.ID_OK:
            self.FileSavingTo = dlg.GetPath()
            self.Path = dlg.GetDirectory()
            self.Filename = dlg.GetFilename().split(".")[0]
            
            self.LoadFile()
            dlg.Close(True)
    
    def OnNew(self, event):
        # New project, new everything
        self.Canvas.ClearCanvas()
        self.RightPanel.CanvasName = "Canvas"
        self.FileSavingTo = None
        self.Path = None
        self.Filename = None
    
    def OnSave(self, event):
        if self.FileSavingTo == None:
            dlg = wx.FileDialog(self, "Open a file", style=wx.FD_SAVE)
            
            wildcard =  "TXT files (.txt)|*.txt|" \
                        "All files (*.*)|*.*"
            dlg.SetWildcard(wildcard)
            #dlg.Show(True)
            dlg.Raise() # This brings the window up for the user to interact with
            
            if dlg.ShowModal() == wx.ID_OK:
                self.FileSavingTo = dlg.GetPath()
                self.Path = dlg.GetDirectory()
                self.Filename = dlg.GetFilename()[:-4]
                
                self.SaveFile()
                
                dlg.Close(True)
        else:
            self.SaveFile()
    
    def OnSaveAs(self, event):
        dlg = wx.FileDialog(self, "Open a file", style=wx.FD_SAVE)
        
        wildcard =  "TXT files (.txt)|*.txt|" \
                    "All files (*.*)|*.*"
        dlg.SetWildcard(wildcard)
        
        dlg.Raise() # This brings the window up for the user to interact with
        
        if dlg.ShowModal() == wx.ID_OK:
            self.FileSavingTo = dlg.GetPath()
            self.Path = dlg.GetDirectory()
            self.Filename = dlg.GetFilename()[:-4]
            
            self.SaveFile()
            
            dlg.Close(True)
    
    def OnSaveImage(self, event):
        dlg = wx.FileDialog(self, "Open a file", style=wx.FD_SAVE)
        
        formats = {}
        formats[0] = {'type': wx.BITMAP_TYPE_JPEG, 'tag': "jpg", 'wildcard': "JPEG files (.jpg)|*.jpg|",}
        formats[formats.keys()[-1] + 1] = {'type': wx.BITMAP_TYPE_PNG, 'tag': "png", 'wildcard': "PNG files (.png)|*.png|",}
        formats[formats.keys()[-1] + 1] = {'type': wx.BITMAP_TYPE_BMP, 'tag': "bmp", 'wildcard': "BMP files (.bmp)|*.bmp|",}
        formats[formats.keys()[-1] + 1] = {'type': wx.BITMAP_TYPE_GIF, 'tag': "gif", 'wildcard': "GIF files (.gif)|*.gif|",}
        formats[formats.keys()[-1] + 1] = {'type': wx.BITMAP_TYPE_TIF, 'tag': "tif", 'wildcard': "TIF files (.tif)|*.tif|",}
        #formats[formats.keys()[-1] + 1] = {'type': wx.BITMAP_TYPE_TGA, 'tag': "tga", 'wildcard': "TGA files (.tga)|*.tga|",} # Not supported by wxPython
        
        dlg.SetWildcard(''.join([formats[type]['wildcard'] for type in formats]))
        
        dlg.Raise() # This brings the window up for the user to interact with
        
        if dlg.ShowModal() == wx.ID_OK:
            picture_full = dlg.GetPath()
            picture_path = dlg.GetDirectory()
            picture_filename = dlg.GetFilename().split(".")[0]
            
            dlg.Close(True)
            
            # Save the image as * with type *.* in location */*.* :D
            #img.SaveFile("%s/%s.%s" % (picture_path, picture_filename, formats[dlg.GetFilterIndex()]['tag']), formats[dlg.GetFilterIndex()]['type'])
            self.SaveImage(picture_path, "%s.%s" % (picture_filename, formats[dlg.GetFilterIndex()]['tag']), formats[dlg.GetFilterIndex()]['type'])
        
    
    def OnSortLinear(self, event):
        self.Canvas.SortLinear()
    
    def OnViewAdvanced(self, event):
        self.ViewType = 2 # Advanced Mode
    
    def OnViewSimple(self, event):
        self.ViewType = 1 # Simple Mode
    
    def RemoveVariable(self, var):
        popped_var = self.Variables.pop(self.Variables.index(var))
        self.Canvas.RemoveVariable(popped_var)
    
    def SaveFile(self):
        pass
    
    def SaveImage(self, path, filename, type):
        x, y = self.Canvas.GetSize()
        img = wx.EmptyBitmap(x, y, -1)
        self.Canvas.GetBitMap(img)
        
        # Save the image as * with type *.* in location */*.* :D
        img.SaveFile("%s/%s" % (path, filename), type)
    
    def SetGroups(self, group):
        self.CurrentGroups = group
    
    def SetVariables(self, vars):
        self.Variables = vars

app = wx.App()

ogl.OGLInitialize()
MainFrame(None, -1, 'Canvas Prototype')

app.MainLoop()
app.Destroy() # Clean up the mess
