import wx
from random import randint

# http://www.zetcode.com/wxpython/ - Best guide out there
# http://wiki.wxpython.org/Getting%20Started - Another useful resource
# http://wiki.wxpython.org/DoubleBufferedDrawing - Best explination about buffering and reducing flicker in graphics

# Lazy way for assigning ID's :P - I don't care what they are, just so long as they're assigned somehow
global _sys_id

_sys_id = 100 # 100 is ignored

def itterID():
    global _sys_id
    _sys_id += 1
    return _sys_id

# ID's for event catching when clicking buttons in the menu
MENU_ID_ABOUT = itterID()
MENU_ID_EXIT = itterID()

# ID's for tools clicked on
TOOL_PLACE_COLOR = itterID()
TOOL_CHANGE_COLOR = itterID()
TOOL_MOVE_BOX = itterID()
TOOL_ALTER_BOX = itterID()
TOOL_DELETE_BOX = itterID()

# This class helps keep track of altering anything on the screen  of interest that can be altered throughout the session
class ColorBox(object):
    def __init__(self, x, y, color, size):
        # Drawing Size
        self.size_x = size[0]
        self.size_y = size[1]
        self.SetPosition(x, y)
        
        self.color = color
        self.id = itterID()
    
    def __repr__(self):
        return "Box # %(id)s at (%(x)s, %(y)s) with size (%(size_x)s, %(size_y)s) having color '%(color)s' has boundaries of (%(bounding_x)s, %(bounding_y)s) - (x, y, z) Notiation" % self.__dict__

    def SetPosition(self, x, y):
        self.x = x - self.size_x / 2
        self.y = y - self.size_y / 2
        
        # Also reassign the boundaries
        self.SetBoundaries()
        
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
        self.MouseButtonBeingHeldDown = False
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        # Can not bind EVT_Motion and EVT_Mouse_Events, the former is ignored in the binds
        # DO NOT USE EVT_MOUSE_EVENTS if you expect to prevent mouse button conflictions with mouse motion draw events.
        # Holding down any mouse button will cause an update to fail due to the configuration of a single mouse event handler
        # self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvents)
        # Always break mouse events apart from each other, other wise you will formulate a bottleneck that prevents any inner application updates from happening
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeft)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRight)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        
        self.SetBackgroundColour('WHITE')
    
    def OnPaint(self, event):
        # Do not put buttons in the with repainting the entire window, the CPU requirements spike hard and hold causing event issues and hanging the program
        dc = wx.PaintDC(self)
        self.DoDrawing(event, dc)
    
    def DoDrawing(self, event=None, dc=None):
        if dc is None:
            dc = wx.ClientDC(self)
        
        mdc = wx.BufferedDC(dc)
        
        mdc.Clear()
        
        mdc.SetPen(wx.Pen('#d4d4d4', width = 0, style = wx.TRANSPARENT))
        
        for group in self.list_of_paintables:
            mdc.SetBrush(wx.Brush(group.color)) # '#c56c00'
            mdc.DrawRectangle(group.x, group.y, group.size_x, group.size_y)
        
        if type(event) == wx.MouseEvent:
            x, y = event.GetPosition()
            mdc.SetPen(wx.Pen(wx.Colour(100, 100, 100), 1, wx.DOT))
            mdc.CrossHair(x, y)
            
        dc.DrawBitmap(mdc.GetAsBitmap(), 0, 0) # Reduces flicker

    def OnEnterWindow(self, event):
        self.DoDrawing() # Repaint everything to simiply fix everything for now
    
    def OnLeaveWindow(self, event):
        self.DoDrawing()  # Repaint everything to simiply fix everything for now
    
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
            else:
                self.tool = TOOL_CHANGE_COLOR
        elif button_id == 4:
            if self.tool == TOOL_MOVE_BOX:
                self.tool = None
            else:
                self.tool = TOOL_MOVE_BOX
        elif button_id == 5:
            if self.tool == TOOL_ALTER_BOX:
                self.tool = None
            else:
                self.tool = TOOL_ALTER_BOX
        elif button_id == 6:
            if self.holdingBox and self.parent.RightPannel.color_text_box.GetValue() != "" and self.parent.RightPannel.size_x_text_box.GetValue() != "" and self.parent.RightPannel.size_y_text_box.GetValue() != "":
                self.holdingBox.color = str(self.parent.RightPannel.color_text_box.GetValue())
                self.holdingBox.SetSize( int(self.parent.RightPannel.size_x_text_box.GetValue()), int(self.parent.RightPannel.size_y_text_box.GetValue()) )
                # Reset everything and repaint everything
                self.parent.RightPannel.ResetFields()
                self.holdingBox = None
                self.DoDrawing()
        elif button_id == 5:
            if self.tool == TOOL_DELETE_BOX:
                self.tool = None
            else:
                self.tool = TOOL_DELETE_BOX
    
    def randomRGBHexString(self):
        r = ""
        
        for item in range(6):
            r += randint(0,15).__hex__()[-1] # return the last character in the string which is the hex value
        
        return r
    
    def OnMouseMotion(self, event):
        self.DoDrawing(event)
    
    def OnMouseLeft(self, event):
        m_pos = event.GetPosition()
        
        if self.tool:
            if self.tool == TOOL_PLACE_COLOR:
                self.list_of_paintables.append(ColorBox(m_pos.x, m_pos.y, self.color, size = (30, 30)))
                self.DoDrawing(event)
            if self.tool == TOOL_CHANGE_COLOR:
                # For all boxes within range down the stack, swap their color out
                for group in self.list_of_paintables:
                    if group.IsPointWithinBoundaries(m_pos.x, m_pos.y):
                        group.color = "#" + self.randomRGBHexString()
                self.DoDrawing(event)
            elif self.tool == TOOL_MOVE_BOX:
                if self.holdingBox == None:
                    pos = 0
                    while self.holdingBox == None and pos < len(self.list_of_paintables):
                        if self.list_of_paintables[-pos - 1].IsPointWithinBoundaries(m_pos.x, m_pos.y):
                            self.holdingBox = self.list_of_paintables.pop(-pos - 1)
                        pos += 1 # Add in a positive notion but traverse the stack in reverse providing a top down selection in the GUI
                    
                    self.DoDrawing(event)
                else: # Place the box
                    self.holdingBox.SetPosition(m_pos.x, m_pos.y)
                    self.list_of_paintables.append(self.holdingBox)
                    self.holdingBox = None
                    self.DoDrawing(event)
            elif self.tool == TOOL_ALTER_BOX:
                pos = 0
                self.holdingBox = None
                self.parent.RightPannel.ResetFields()
                while self.holdingBox == None and pos < len(self.list_of_paintables):
                    if self.list_of_paintables[-pos - 1].IsPointWithinBoundaries(m_pos.x, m_pos.y):
                        self.holdingBox = self.list_of_paintables[-pos - 1]
                    pos += 1 # Add in a positive notion but traverse the stack in reverse providing a top down selection in the GUI
                
                if self.holdingBox:
                    self.parent.RightPannel.color_text_box.SetValue(self.holdingBox.color)
                    self.parent.RightPannel.size_x_text_box.SetValue(str(self.holdingBox.size_x))
                    self.parent.RightPannel.size_y_text_box.SetValue(str(self.holdingBox.size_y))
    
    def OnMouseRight(self, event):
        self.tool = None
        self.color = None
        self.holdingBox = None

class LeftButtonPannel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        self.parent = parent
        
        # GUI Buttons that the user can click on
        wx.Button(self, 1, 'Random Color', (0, 10))
        wx.Button(self, 2, 'Clear Canvas', (0, 50))
        wx.Button(self, 3, 'Change Color', (0, 90))
        #wx.Button(self, 4, 'Move Box', (0, 130))
        wx.Button(self, 5, 'Alter Box', (0, 170))
        wx.Button(self, 6, 'Delete Box', (0, 210))
        
        # Binds for button events
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=1)
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=2)
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=3)
        #self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=4)
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=5)
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=6)

class RightPannel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        self.parent = parent
        
        self.color_text_box = wx.TextCtrl(self, 1, pos = (0,0), size = (130, 25))
        self.size_x_text_box = wx.TextCtrl(self, 2, pos = (0,25), size = (65, 25))
        self.size_y_text_box = wx.TextCtrl(self, 3, pos = (65,25), size = (65, 25))
        
        wx.Button(self, 6, 'Save Changes', (0, 70))
        
        self.Bind(wx.EVT_BUTTON, parent.Canvas.OnButtonClick, id=6)
    
    def ResetFields(self):
        self.color_text_box.SetValue("")
        self.size_x_text_box.SetValue("")
        self.size_y_text_box.SetValue("")

class FirstTest(wx.Frame):
    def __init__(self, parent, id, title, size = (800, 640) ):
        wx.Frame.__init__(self, parent, id, title, pos = (0,0), size = size)
        
        self.Canvas = Canvas(self, 1)
        self.LeftButtonPannel = LeftButtonPannel(self, 2)
        self.RightPannel = RightPannel(self, 3)
        
        #self.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))
        
        # Setting up the menu.
        filemenu = wx.Menu()
        filemenu.Append(MENU_ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(MENU_ID_EXIT,"E&xit"," Terminate the program")
        
        # Build and add the entire menu bar to the window
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)
        
        # Bind events to methods
        self.Bind(wx.EVT_LEAVE_WINDOW, self.Canvas.OnLeaveWindow)
        self.Bind(wx.EVT_ENTER_WINDOW, self.Canvas.OnEnterWindow)
        
        # Bind menu events to methods
        wx.EVT_MENU(self, MENU_ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, MENU_ID_EXIT, self.OnExit)
        
        # Create inner box that will contain the buttons
        #self.ButtonSizer = wx.BoxSizer(wx.VERTICAL)
        #self.ButtonSizer.Add(wx.Button(self, 1, 'Blue', (10, 10)), 1)
        #self.ButtonSizer.Add(wx.Button(self, 2, 'Red', (10, 50)), 1)
        
        # Create base layer of the window to assign a size to
        self.layoutSizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.layoutSizer.Add(self.ButtonSizer, 1, wx.EXPAND)
        
        self.layoutSizer.Add(self.LeftButtonPannel, 0, wx.VERTICAL)
        self.layoutSizer.Add(self.Canvas, 4, wx.VERTICAL | wx.HORIZONTAL | wx.EXPAND)
        self.layoutSizer.Add(self.RightPannel, 1, wx.RIGHT | wx.VERTICAL)
        
        # Assign the base layer to the window
        self.SetSizer(self.layoutSizer)
        self.SetAutoLayout(1)
        # Using this resets the size of the window which is not what I want right now
        #self.layoutSizer.Fit(self)
        # Simplifies setting Sizer, Setting Auto Layout and fitting the window to the sizer
        
        #self.SetSizerAndFit(self.layoutSizer) 
        
        self.Centre()
        self.Show(True)
    
    def OnAbout(self, event):
        dialog = wx.MessageDialog(self, "This is only a prototype for designing a GUI around the CSV to XML convertor","Prototype Help", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    
    def OnExit(self, event):
        self.Close(True)

app = wx.App()

FirstTest(None, -1, 'Woot :D')

app.MainLoop()
