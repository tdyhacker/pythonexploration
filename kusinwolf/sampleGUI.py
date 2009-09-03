import wx
from random import randint

# http://www.zetcode.com/wxpython/ - Best guide out there
# http://wiki.wxpython.org/Getting%20Started - Another useful resource
# http://wiki.wxpython.org/DoubleBufferedDrawing - Best explination about buffering and reducing flicker in graphics

# Lazy way for assigning ID's :P - I don't care what they are, just so long as they're assigned somehow
global _sys_id
global _obj_id

_sys_id = 100 # 100 is ignored
_obj_id = 1000 # 100 is ignored

def itterID():
    global _sys_id
    _sys_id += 1
    return _sys_id

def objItterID():
    global _sys_id
    _sys_id += 1
    return _sys_id

# ID's for event catching when clicking buttons in the menu
MENU_ID_ABOUT = itterID()
MENU_ID_SAVE = itterID()
MENU_ID_SAVEAS = itterID()
MENU_ID_LOAD = itterID()
MENU_ID_EXIT = itterID()

# ID's for tools clicked on
TOOL_PLACE_COLOR = itterID()
TOOL_CHANGE_COLOR = itterID()
TOOL_LINK_BOX = itterID()
TOOL_ALTER_BOX = itterID()
TOOL_DELETE_BOX = itterID()

# This class helps keep track of altering anything on the screen  of interest that can be altered throughout the session
class ColorBox(object):
    def __init__(self, x, y, color, size, pointsTo = None):
        # Drawing Size
        self.size_x = size[0]
        self.size_y = size[1]
        self.SetPosition(x, y)
        
        self.color = color
        self.id = objItterID()
        self.pointsTo = pointsTo
    
    def __repr__(self):
        return "Box # %(id)s at (%(x)s, %(y)s) with size (%(size_x)s, %(size_y)s) having color '%(color)s' has boundaries of (%(bounding_x)s, %(bounding_y)s) - (x, y, z) Notiation" % self.__dict__

    def save(self):
            
        return "%(x)s, %(y)s, %(size_x)s, %(size_y)s, %(color)s" % self.__dict__

    def SetPosition(self, x, y):
        self.x = x - self.size_x / 2
        self.y = y - self.size_y / 2
        
        # Also reassign the boundaries
        self.SetBoundaries()
    
    def GetCenter(self):
        return wx.Point(x = (self.x + self.size_x / 2), y = (self.y + self.size_y / 2))
    
    def SetSize(self, x, y):
        self.size_x = x
        self.size_y = y
        
        # Also reassign the boundaries
        self.SetBoundaries()
    
    def SetBoundaries(self):
        # Tuples of the bounding boxes
        self.bounding_x = ((self.x), (self.x + (self.size_x)))
        self.bounding_y = ((self.y), (self.y + (self.size_y)))
        
        # If the values are not in least to greatest order, then IsPointWithinBoundaries would always return false
        self.bounding_x = list(self.bounding_x)
        self.bounding_x.sort()
        self.bounding_x = tuple(self.bounding_x)
        
        self.bounding_y = list(self.bounding_y)
        self.bounding_y.sort()
        self.bounding_y = tuple(self.bounding_y)
    
    def IsPointWithinBoundaries(self, x, y):
        if (x >= self.bounding_x[0] and x <= self.bounding_x[1]) and (y >= self.bounding_y[0] and y <= self.bounding_y[1]):
            return True
        else:
            return False

class Canvas(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        self.parent = parent
        self.list_of_paintables = []
        self.color = None
        self.tool = None
        self.holdingBox = None
        self.LastClickedOn = None
        self.MouseButtonBeingHeldDown = False
        self.LinkObjectOne = None
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # Can not bind EVT_Motion and EVT_Mouse_Events, the former is ignored in the binds
        # DO NOT USE EVT_MOUSE_EVENTS if you expect to prevent mouse button conflictions with mouse motion draw events.
        # Holding down any mouse button will cause an update to fail due to the configuration of a single mouse event handler
        #self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)
        # Always break mouse events apart from each other, other wise you will formulate a bottleneck that prevents any inner application updates from happening
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        # Bind events to methods
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        
        self.SetBackgroundColour('WHITE')
    
    def randomRGBHexString(self):        
        return str().join([randint(0,15).__hex__()[-1] for item in range(6)]) # return the last character in the string which is the hex value
    
    def OnPaint(self, event):
        # Do not put buttons in the with repainting the entire window, the CPU requirements spike hard and hold causing event issues and hanging the program
        dc = wx.PaintDC(self)
        self.DoDrawing(event, dc)
    
    def DoDrawing(self, event=None, dc=None):
        if dc is None:
            dc = wx.ClientDC(self)
        
        mdc = wx.BufferedDC(dc, self.parent.GetSize()) # Only paints on the space that is shown
        
        mdc.Clear()
        
        if type(event) == wx.MouseEvent:
            x, y = event.GetPosition()
            
            # Draw the line from the moving box to where it points to
            if self.holdingBox != None and self.tool == None and self.holdingBox.pointsTo:
                mdc.SetPen(wx.Pen('#000000', width = 1))
                mdc.DrawLine(self.holdingBox.GetCenter().x, self.holdingBox.GetCenter().y, self.holdingBox.pointsTo.GetCenter().x, self.holdingBox.pointsTo.GetCenter().y)
        
        # Paint all the lines between each object
        mdc.SetPen(wx.Pen('#000000', width = 1))
        for group in self.list_of_paintables:
            if group.pointsTo:
                mdc.DrawLine(group.GetCenter().x, group.GetCenter().y, group.pointsTo.GetCenter().x, group.pointsTo.GetCenter().y)
        
        # Paint all the objects
        mdc.SetPen(wx.Pen('#d4d4d4', width = 0, style = wx.TRANSPARENT))
        for group in self.list_of_paintables:
            mdc.SetBrush(wx.Brush(group.color)) # '#c56c00'
            mdc.DrawRectangle(group.x, group.y, group.size_x, group.size_y)
        
        if type(event) == wx.MouseEvent:
            
            if self.color != None and self.tool == TOOL_PLACE_COLOR:
                mdc.SetPen(wx.Pen('#d4d4d4', width = 0, style = wx.TRANSPARENT))
                mdc.SetBrush(wx.Brush(self.color))
                mdc.DrawRectangle(x - 15, y - 15, 30, 30)
            elif self.holdingBox != None and self.tool == None:
                
                # Paint the object on the cursor to show it's current position
                mdc.SetPen(wx.Pen('#d4d4d4', width = 0, style = wx.TRANSPARENT))
                mdc.SetBrush(wx.Brush(self.holdingBox.color))
                mdc.DrawRectangle(x - (self.holdingBox.size_x / 2), y - (self.holdingBox.size_y / 2), self.holdingBox.size_x, self.holdingBox.size_y)
            
            # Cool features with the mouse :D
            #mdc.SetPen(wx.Pen(wx.Colour(100, 100, 100), 1, wx.DOT))
            #mdc.CrossHair(x, y)
            
            # Draw the current coordinates next to the cursor
            #mdc.DrawText("x: %s, y: %s" % (x, y), x + 5, y - 20)
        
        dc.DrawBitmap(mdc.GetAsBitmap(self.parent.GetRect()), 0, 0) # Reduces flicker and reduces loading time of the bitmap from the background

    def OnEnterWindow(self, event):
        self.DoDrawing() # Repaint everything to simiply fix everything for now
    
    def OnLeaveWindow(self, event):
        self.DoDrawing()  # Repaint everything to simiply fix everything for now
    
    def OnMouseMotion(self, event):
        m_pos = event.GetPosition()
        if self.holdingBox:
            self.holdingBox.SetPosition(m_pos.x, m_pos.y)
            self.parent.RightPanel.UpdatePositionFields(event.GetPosition())
        
        if self.tool == None:
            if self.getBelowMouse(event):
                self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            else:
                self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        
        self.DoDrawing(event)
    
    def getBelowMouse(self, event, pop=False):
        item = None
        pos = 0
        m_pos = event.GetPosition()
        
        while item == None and pos < len(self.list_of_paintables):
            if self.list_of_paintables[-pos - 1].IsPointWithinBoundaries(m_pos.x, m_pos.y):
                if pop:
                    item = self.list_of_paintables.pop(-pos - 1)
                else:
                    item = self.list_of_paintables[-pos - 1]
            pos += 1 # Add in a positive notion but traverse the stack in reverse providing a top down selection in the GUI
        
        return item
    
    def OnMouseLeftDown(self, event):
        m_pos = event.GetPosition()
        
        if self.tool:
            if self.tool == TOOL_PLACE_COLOR:
                self.list_of_paintables.append(ColorBox(m_pos.x, m_pos.y, self.color, size = (30, 30)))
                
            elif self.tool == TOOL_CHANGE_COLOR:
                # For all boxes within range down the stack, swap their color out
                for group in self.list_of_paintables:
                    if group.IsPointWithinBoundaries(m_pos.x, m_pos.y):
                        group.color = "#" + self.randomRGBHexString()
                
            elif self.tool == TOOL_DELETE_BOX:
                removing = self.getBelowMouse(event, pop=True) # Just delete the object from the list
                for item in self.list_of_paintables:
                    if item.pointsTo == removing:
                        item.pointsTo = None # Clear out all of the boxes' pointTos when I remove a box that is being pointed to
                
            elif self.tool == TOOL_LINK_BOX:
                if self.LinkObjectOne == None:
                    self.LinkObjectOne = self.getBelowMouse(event, pop=False)
                else:
                    self.LinkObjectOne.pointsTo = self.getBelowMouse(event, pop=False)
                    self.LinkObjectOne = None
            
        elif self.tool == None:
            self.holdingBox = self.getBelowMouse(event, True)
            
            self.parent.RightPanel.ResetFields()
            
            if self.holdingBox:
                # Display the attributes in the area
                self.parent.RightPanel.AssignObjectToFields(self.holdingBox)
                
                self.LastClickedOn = self.holdingBox # This helps keep track of what we want to alter
    
    def OnMouseLeftUp(self, event):
        m_pos = event.GetPosition()
        
        if self.tool == None and self.holdingBox != None:
            self.holdingBox.SetPosition(m_pos.x, m_pos.y)
            self.list_of_paintables.append(self.holdingBox)
            self.holdingBox = None
    
    def OnMouseRightDown(self, event):
        self.tool = None
        self.color = None
        self.holdingBox = None
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
    
    def OnButtonClick(self, event):
        button = event.GetEventObject()
        button_id = button.GetId()
        
        if button_id == 1:
            # Reset all buttons
            
            self.tool = TOOL_PLACE_COLOR
            self.color = "#" + self.randomRGBHexString()
            
        elif button_id == 2:
            self.list_of_paintables = []
            self.DoDrawing()
        elif button_id == 3:
            if self.tool == TOOL_CHANGE_COLOR:
                self.tool = None
                self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            else:
                self.tool = TOOL_CHANGE_COLOR
                self.SetCursor(wx.StockCursor(wx.CURSOR_SPRAYCAN))
        elif button_id == 4:
            if self.tool == TOOL_LINK_BOX:
                self.tool = None
                self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            else:
                self.tool = TOOL_LINK_BOX
                self.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))
        elif button_id == 5:
            if self.tool == TOOL_ALTER_BOX:
                self.tool = None
                self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            else:
                self.tool = TOOL_ALTER_BOX
        elif button_id == 6:
            if self.LastClickedOn:
                self.parent.RightPanel.AssignFieldsToObject(self.LastClickedOn)
                
                # Reset everything and repaint everything
                self.parent.RightPanel.ResetFields()
                self.LastClickedOn = None
                self.DoDrawing()
        elif button_id == 7:
            if self.tool == TOOL_DELETE_BOX:
                self.tool = None
                self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            else:
                self.tool = TOOL_DELETE_BOX
                self.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))

class LeftButtonPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        self.parent = parent
        
        # GUI Buttons that the user can click on
        wx.Button(self, 1, 'Random Color', (0, 10))
        wx.Button(self, 2, 'Clear Canvas', (0, 50))
        wx.Button(self, 3, 'Change Color', (0, 90))
        wx.Button(self, 4, 'Link', (0, 130))
        #wx.Button(self, 5, 'Alter Box', (0, 170))
        #--wx.Button(self, 6, 'Save Changes', (0, 70)) # Located in the RightPanel
        wx.Button(self, 7, 'Delete Box', (0, 210))
        
        # Binds for button events
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=1)
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=2)
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=3)
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=4)
        #self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=5)
        #--self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=6) # Located in the RightPanel
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=7)

class RightPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        self.parent = parent
        
        self.color_text_box = wx.TextCtrl(self, 1, pos = (0,0), size = (130, 25))
        self.size_x_text_box = wx.TextCtrl(self, 2, pos = (0,25), size = (65, 25))
        self.size_y_text_box = wx.TextCtrl(self, 3, pos = (65,25), size = (65, 25))
        self.x_text_box = wx.TextCtrl(self, 4, pos = (0,50), size = (65, 25))
        self.y_text_box = wx.TextCtrl(self, 5, pos = (65,50), size = (65, 25))
        
        wx.Button(self, 6, 'Save Changes', (0, 70))
        
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=6)
    
    def ResetFields(self):
        self.color_text_box.SetValue("")
        self.size_x_text_box.SetValue("")
        self.size_y_text_box.SetValue("")
        self.x_text_box.SetValue("")
        self.y_text_box.SetValue("")
    
    def AssignObjectToFields(self, obj):
        self.color_text_box.SetValue(str(obj.color))
        self.size_x_text_box.SetValue(str(obj.size_x))
        self.size_y_text_box.SetValue(str(obj.size_y))
        self.x_text_box.SetValue(str(obj.x))
        self.y_text_box.SetValue(str(obj.y))
    
    def UpdatePositionFields(self, obj):
        self.x_text_box.SetValue(str(obj.x))
        self.y_text_box.SetValue(str(obj.y))
    
    def AssignFieldsToObject(self, obj):
        if self.color_text_box.GetValue():
            obj.color = str(self.color_text_box.GetValue())
        if self.size_x_text_box.GetValue() and self.size_y_text_box.GetValue():
            obj.SetSize( int(self.size_x_text_box.GetValue()), int(self.size_y_text_box.GetValue()) )
        if self.x_text_box.GetValue() and self.y_text_box.GetValue():
            obj.SetPosition( int(self.x_text_box.GetValue()), int(self.y_text_box.GetValue()) )

class FirstTest(wx.Frame):
    def __init__(self, parent, id, title, size = (800, 640) ):
        wx.Frame.__init__(self, parent, id, title, pos = (0,0), size = size)
        
        self.FileSavingTo = None
        
        self.Canvas = Canvas(self, 1)
        self.LeftButtonPanel = LeftButtonPanel(self, 2)
        self.RightPanel = RightPanel(self, 3)
        
        #self.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))
        
        # File menu.
        filemenu = wx.Menu()
        filemenu.Append(MENU_ID_SAVE, "&Save"," Save current canvas")
        filemenu.Append(MENU_ID_SAVE, "Save &As..."," Save current canvas to a new file")
        filemenu.Append(MENU_ID_LOAD, "&Load"," Load existing canvas")
        filemenu.AppendSeparator()
        filemenu.Append(MENU_ID_EXIT,"E&xit"," Terminate the program")
        
        # Help Menu
        helpmenu = wx.Menu()
        helpmenu.Append(MENU_ID_ABOUT, "&About"," Information about this program")
        
        # Build and add the entire menu bar to the window
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
        
        # Bind menu events to methods
        wx.EVT_MENU(self, MENU_ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, MENU_ID_SAVE, self.OnSave)
        wx.EVT_MENU(self, MENU_ID_SAVEAS, self.OnSaveAs)
        wx.EVT_MENU(self, MENU_ID_LOAD, self.OnLoad)
        wx.EVT_MENU(self, MENU_ID_EXIT, self.OnExit)
        
        # Create inner box that will contain the buttons
        #self.ButtonSizer = wx.BoxSizer(wx.VERTICAL)
        #self.ButtonSizer.Add(wx.Button(self, 1, 'Blue', (10, 10)), 1)
        #self.ButtonSizer.Add(wx.Button(self, 2, 'Red', (10, 50)), 1)
        
        # Create base layer of the window to assign a size to
        self.layoutSizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.layoutSizer.Add(self.ButtonSizer, 1, wx.EXPAND)
        
        self.layoutSizer.Add(self.LeftButtonPanel, 0, wx.VERTICAL)
        self.layoutSizer.Add(self.Canvas, 4, wx.VERTICAL | wx.HORIZONTAL | wx.EXPAND)
        self.layoutSizer.Add(self.RightPanel, 1, wx.RIGHT | wx.VERTICAL)
        
        # Assign the base layer to the window
        self.SetSizer(self.layoutSizer)
        self.SetAutoLayout(1)
        # Using this resets the size of the window which is not what I want right now
        #self.layoutSizer.Fit(self)
        # Simplifies setting Sizer, Setting Auto Layout and fitting the window to the sizer
        
        #self.SetSizerAndFit(self.layoutSizer) 
        
        self.Centre()
        self.Show(True)
        
    def SaveFile(self):
        file = open(self.FileSavingTo, "w")
        
        for item in self.Canvas.list_of_paintables:
            pT = -1
            if item.pointsTo:
                pT = self.Canvas.list_of_paintables.index(item.pointsTo)
                
            file.write("%s, %s\n" % (item.save(), pT))
        
        file.close()
    
    def LoadFile(self):
        file = open(self.FileSavingTo, "r")
        
        self.Canvas.list_of_paintables = []
        
        for line in file.readlines():
            tempLine = line[:].replace("\n", '') # Peform an exact copy of the list
            line = [] # reset the list
            for item in tempLine.split(", "):
                try:
                    # If you use str.isdigit() it will return false for negative numbers which is a huge problem
                    line.append(int(item))
                except ValueError:
                    # The value was not an integer
                    line.append(item) # Remove the endline
            
            self.Canvas.list_of_paintables.append(ColorBox(x = line[0], y = line[1], size = (line[2], line[3]), color = line[4], pointsTo = line[5]))
            
        for box in self.Canvas.list_of_paintables:
            if box.pointsTo != -1:
                box.pointsTo = self.Canvas.list_of_paintables[box.pointsTo]
            else:
                box.pointsTo = None # reset the value
            
        file.close()
    
    def OnSave(self, event):
        if self.FileSavingTo == None:
            dlg = wx.FileDialog(self, "Open a file", style=wx.FD_SAVE)
            
            wildcard =  "Text files (.txt)|*.txt|"   \
                        "All files (*.*)|*.*"
            dlg.SetWildcard(wildcard)
            #dlg.Show(True)
            dlg.Raise() # This brings the window up for the user to interact with
            
            if dlg.ShowModal() == wx.ID_OK:
                self.FileSavingTo = dlg.GetPath()
                
                self.SaveFile()
                
                dlg.Close(True)
            #elif dlg.ShowModal() == wx.ID_CANCEL:
            #    dlg.Close(True)
        else:
            self.SaveFile()
    
    def OnSaveAs(self, event):
        dlg = wx.FileDialog(self, "Open a file", style=wx.FD_SAVE)
        
        wildcard =  "Text files (.txt)|*.txt|"   \
                    "All files (*.*)|*.*"
        dlg.SetWildcard(wildcard)
        #dlg.Show(True)
        dlg.Raise() # This brings the window up for the user to interact with
        
        if dlg.ShowModal() == wx.ID_OK:
            self.FileSavingTo = dlg.GetPath()
            
            self.SaveFile()
            
            dlg.Close(True)

    def OnLoad(self, event):
        dlg = wx.FileDialog(self, "Open a file", style=wx.FD_OPEN)
        
        wildcard =  "Text files (.txt)|*.txt|"   \
                    "All files (*.*)|*.*"
        dlg.SetWildcard(wildcard)
        #dlg.Show(True)
        dlg.Raise() # This brings the window up for the user to interact with
        
        if dlg.ShowModal() == wx.ID_OK:
            self.FileSavingTo = dlg.GetPath()
            self.LoadFile()
            dlg.Close(True)
        #elif dlg.ShowModal() == wx.ID_CANCEL:
        #    dlg.Close(True)
    
    
    def OnAbout(self, event):
        dialog = wx.MessageDialog(self, "This is only a prototype for designing a GUI","Prototype Help", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    
    def OnExit(self, event):
        self.Close(True)

app = wx.App()

FirstTest(None, -1, 'Woot :D')

app.MainLoop()
