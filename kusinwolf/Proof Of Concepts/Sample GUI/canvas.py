from globals import *
from classes import *
import math

class Canvas(wx.ScrolledWindow):
    def __init__(self, parent, id):
        wx.ScrolledWindow.__init__(self, parent, id)
        
        self.parent = parent
        self.CanvasObjects = []
        self.color = None
        self.tool = None
        self.holdingBox = None
        self.LastClickedOn = None
        self.MouseButtonBeingHeldDown = False
        self.x_offset = None
        self.y_offset = None
        self.copied = None
        
        # This helps keep track of how large the canvas needs to be
        self.largest_x = 0
        self.largest_y = 0
        
        self.SetScrollbars(10, 10, 0, 0)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
    
    def AddCanvasObject(self, interactable):
        self.CanvasObjects.append(interactable)
    
    def ClearCanvas(self):
        self.CanvasObjects = [] # Clear the board
        self.ResetLastClickedOn()
        
        self.parent.SetGroups([]) # Clear everything
        self.DoDrawing()
    
    def DoDrawing(self, event=None, dc=None):
        #def DrawArrow(surface, obj):
        #    # Arrow calculations
        #    center_of_line = wx.Point(x = (obj.GetCenter().x + obj.pointsTo.GetCenter().x) / 2, y = (obj.GetCenter().y + obj.pointsTo.GetCenter().y) / 2)
        #    point_to_point_angle = math.degrees(math.atan2((obj.GetCenter().y - obj.pointsTo.GetCenter().y), (obj.GetCenter().x - obj.pointsTo.GetCenter().x)))
        #    
        #    if point_to_point_angle != 0:
        #        sign = point_to_point_angle / abs(point_to_point_angle) # Either will be 1 or -1
        #    else:
        #        sign = 1
        #    
        #    arrow_length = 10
        #    
        #    x1 = center_of_line.x #obj.GetCenter().x
        #    x0 = obj.pointsTo.GetCenter().x
        #    y1 = center_of_line.y #obj.GetCenter().y
        #    y0 = obj.pointsTo.GetCenter().y
        #    if x1 == x0:
        #        m = (y1 - y0) / 1
        #    else:
        #        m = (y1 - y0) / (x1 - x0) # Slope
        #        
        #    t = 45 # Degrees from the slope to draw from
        #    t = point_to_point_angle
        #    n = math.atan(t * math.pi / 180) #1 / math.sqrt(3) # ?
        #    #if x1 < x0:
        #    #    d = -10
        #    #else:
        #    d = -20 # Length of line
        #    
        #    if x1 != x0 or y1 != y0:
        #        #end_x1 = x1 - ((x1-x0) * math.cos(t) - (y1-y0) * math.sin(t)) * d / math.sqrt(math.pow((x1-x0), 2) + math.pow((y1-y0), 2))
        #        #end_y1 = y1 - ((y1-y0) * math.cos(t) - (x1-x0) * math.sin(t)) * d / math.sqrt(math.pow((x1-x0), 2) + math.pow((y1-y0), 2))
        #        #
        #        #end_x2 = x1 + ((x1-x0) * math.cos(t) - (y1-y0) * math.sin(t)) * d / math.sqrt(math.pow((x1-x0), 2) + math.pow((y1-y0), 2))
        #        #end_y2 = y1 - ((y1-y0) * math.cos(t) - (x1-x0) * math.sin(t)) * d / math.sqrt(math.pow((x1-x0), 2) + math.pow((y1-y0), 2))
        #        
        #        end_x1 = x1 - (((x1 - x0) - n * (y1 - y0)) / math.sqrt((1 + math.pow(n, 2)))) * ( d / math.sqrt(math.pow((x1-x0), 2) + math.pow((y1-y0), 2)))
        #        end_y1 = y1 - (((y1 - y0) - n * (x1 - x0)) / math.sqrt((1 + math.pow(n, 2)))) * ( d / math.sqrt(math.pow((x1-x0), 2) + math.pow((y1-y0), 2)))
        #    
        #        end_x2 = x1 - (((x1 - x0) + n * (y1 - y0)) / math.sqrt((1 + math.pow(n, 2)))) * ( d / math.sqrt(math.pow((x1-x0), 2) + math.pow((y1-y0), 2)))
        #        end_y2 = y1 - (((y1 - y0) + n * (x1 - x0)) / math.sqrt((1 + math.pow(n, 2)))) * ( d / math.sqrt(math.pow((x1-x0), 2) + math.pow((y1-y0), 2)))
        #    
        #        surface.DrawLine(obj.GetCenter().x, obj.GetCenter().y, obj.pointsTo.GetCenter().x, obj.pointsTo.GetCenter().y)
        #    
        #        # Draw Arrow
        #        surface.DrawLine( x1, y1, end_x1, end_y1)
        #        surface.DrawLine( x1, y1, end_x2, end_y2 )
        #        
        #        # Cool features with the mouse :D
        #        #surface.SetPen(wx.Pen(wx.Colour(100, 100, 100), 1, wx.DOT))
        #        #surface.CrossHair(x, y)
        #        
        #        # Draw the current values next to the box
        #        surface.DrawText("top: %.3f\nangle: %.3f\nn: %.3f" % (((x1 - x0) - n * (y1 - y0)), point_to_point_angle, math.atan((point_to_point_angle * math.pi / 180))), 20, 20)
        
        def DrawGroups(surface, size, lanes):
            if lanes:
                xy_pos = 0
                width = size[0]
                length = size[1]
                portion = width / len(lanes)
                
                if self.GetFlippedGroups():
                    surface.DrawLine(45, 0, 45, length) # Draw Vertical line
                    surface.DrawLine(0, length - 1, width, length - 1) # Draw last verticle line
                else:
                    surface.DrawLine(0, 45, width, 45) # Draw horizontal line
                    surface.DrawLine(width - 1, 0, width - 1, length) # Draw last verticle line
                    
                for lane in lanes:
                    if self.GetFlippedGroups(): # Horizontal lines
                        surface.DrawRotatedText(lane, 20, ((portion / 2) + xy_pos), 90) # Display the task name
                        surface.DrawLine(0, xy_pos, width, xy_pos) # Draw verticle line
                    else: # Vertical Lines
                        surface.DrawText(lane, ((portion / 2) + xy_pos - ((len(lane) / 3) * 25)), 20) # Display the task name
                        surface.DrawLine(xy_pos, 0, xy_pos, length) # Draw verticle line
                    xy_pos += portion
        
        if dc is None:
            dc = wx.ClientDC(self)
        
        # Create a background canvas to paint on and clear it
        mdc = wx.BufferedDC(dc, self.parent.GetSize()) # Only paints on the space that is shown
        mdc.Clear()
        
        self.PrepareDC(mdc) # Prepares the scrolling image to be drawn on without causing problems
        
        # Group Columns
        DrawGroups(mdc, self.GetSize(), self.GetGroups())
        
        if type(event) == wx.MouseEvent:
            x, y = event.GetPosition()
            
            # Draw the line from the moving box to where it points to
            if self.holdingBox != None and self.tool == None:
                #DrawArrow(mdc, self.holdingBox)
                self.holdingBox.DrawLines(mdc)
            
            if self.LastClickedOn != None and self.tool == TOOL_LINK:
                mdc.DrawLine(self.LastClickedOn.GetCenter().x, self.LastClickedOn.GetCenter().y, x, y)
            
        # Helps to find positions
        #mdc.DrawText("x: %d\ny: %d\ns: %s" % (self.GetScrollPos(1), self.GetScrollPos(-1), self.GetRect()), 20, 20) # Display the task name
        
        # Paint all the lines between each object
        mdc.SetPen(wx.Pen('#000000', width = 1))
        for group in self.CanvasObjects:
            group.DrawLines(mdc)
            #DrawArrow(mdc, group)
        
        # Paint all the objects
        for group in self.CanvasObjects:
            group.Render(mdc) # Let the objects render themselves
        
        if type(event) == wx.MouseEvent:
            if self.tool in [TOOL_PLACE_SQUARE, TOOL_PLACE_TRIANGLE]:
                #### THERE IS SOMETHING FAILING RIGHT HERE -- For some reason any objects on the Canvas with the same class are having the default
                #### variables added back into their mix every time I move the mouse - WHY?!
                if self.tool == TOOL_PLACE_SQUARE:
                    obj = Square
                elif self.tool == TOOL_PLACE_TRIANGLE:
                    obj = Triangle
                
                obj(self, event.GetPosition(), color = self.color, size = (30, 30)).Render(mdc)
            
            elif self.holdingBox != None and self.tool == None:
                # Paint the object on the cursor to show it's current position
                self.holdingBox.Render(mdc)
        
        dc.DrawBitmap(mdc.GetAsBitmap(self.parent.GetRect()), 0, 0) # Reduces flicker and reduces loading time of the bitmap from the background
    
    def GetBelowMouse(self, event, pop=False):
        item = None
        pos = 0
        m_pos = event.GetPosition()
        
        while item == None and pos < len(self.CanvasObjects):
            if self.CanvasObjects[-pos - 1].IsBeneathMouse(m_pos):
                if pop:
                    item = self.CanvasObjects.pop(-pos - 1)
                else:
                    item = self.CanvasObjects[-pos - 1]
            pos += 1 # Add in a positive notion but traverse the stack in reverse providing a top down selection in the GUI
        
        return item
    
    def GetBitMap(self, bitmap):
        def DrawGroups(surface, size, lanes):
            if lanes:
                x_pos = 0
                width = size[0]
                length = size[1]
                portion = width / len(lanes)
                surface.DrawLine(0, 45, width, 45) # Draw horizontal line
                for lane in lanes:
                    surface.DrawText(lane, ((portion / 2) + x_pos - ((len(lane) / 3) * 25)), 20) # Display the task name
                    surface.DrawLine(x_pos, 0, x_pos, length) # Draw verticle line
                    x_pos += portion
                    
                surface.DrawLine(width - 1, 0, width - 1, length) # Draw last verticle line
        
        # Create a background canvas to paint on and clear it
        mdc = wx.MemoryDC() # Only paints on the space that is shown
        mdc.SelectObject(bitmap)
        mdc.Clear()
        
        # Group Columns
        DrawGroups(mdc, self.GetSize(), self.GetGroups())
        
        mdc.SetPen(wx.Pen('#000000', width = 1))
        for group in self.CanvasObjects:
            group.DrawLines(mdc)
            #DrawArrow(mdc, group)
        
        # Paint all the objects
        for group in self.CanvasObjects:
            group.Render(mdc) # Let the objects render themselves
        
        return mdc.GetAsBitmap(self.parent.GetRect())
    
    def GetFlippedGroups(self):
        return self.parent.GetFlippedGroups()
    
    def GetLastClickedOn(self):
        return self.LastClickedOn

    def GetObjects(self):
        return self.CanvasObjects
    
    def GetPointedToInteractable(self, linkTo):
        pos = 0
        found = None
        while pos < len(self.CanvasObjects) and found == None:
            if str(self.CanvasObjects[pos].GetName()) == str(linkTo.to):
                found = self.CanvasObjects[pos]
            
            pos += 1
        
        return found
    
    def GetPointWithinCanvas(self, x, y):
        width, length = self.GetSize()
        
        new_pos = wx.Point(x , y)
        
        if new_pos.x > self.largest_x:
            self.largest_x = new_pos.x
        if new_pos.y > self.largest_y:
            self.largest_y = new_pos.y
        
        #if self.largest_x > width:
        #    self.SetSize(wx.Size(self.largest_x, length))
        #if self.largest_y > length:
        #    self.SetSize(wx.Size(width, self.largest_y))
        
        wx_size, wy_size = self.GetSize()
        self.SetScrollbars(10, 10, (self.largest_x / 10), (self.largest_y / 10)) # seems to be perfect values
        
        #if new_pos.x > width:
        #    new_pos.x = width
        #elif new_pos.x < 0:
        #    new_pos.x = 0
        #if new_pos.y > length:
        #    new_pos.y = length
        #elif new_pos.y < 0:
        #    new_pos.y = 0
        
        return new_pos
    
    def GetGroups(self):
        return self.parent.GetGroups()
    
    def OnButtonClick(self, event):
        button = event.GetEventObject()
        button_id = button.GetId()
        
        if button_id == 1:
            self.tool = TOOL_PLACE_SQUARE
            self.color = "#" + self.RandomRGBHexString()
            self.ResetLastClickedOn()
        
        elif button_id == 2:
            self.tool = TOOL_PLACE_TRIANGLE
            self.color = "#" + self.RandomRGBHexString()
            self.ResetLastClickedOn()
        
        elif button_id == 3:
            self.tool = TOOL_LINK
            self.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))
            self.ResetLastClickedOn()

    def OnEnterWindow(self, event):
        self.DoDrawing() # Repaint everything to simiply fix everything for now
    
    def OnCopy(self, event):
        if self.GetLastClickedOn():
            self.copied = self.GetLastClickedOn().GetCopy()
            self.copied.SetPosition(self.copied.x + 25, self.copied.y + 25)
    
    def OnDelete(self, event):
        if self.GetLastClickedOn():
            
            new_list = self.GetObjects()
            new_list.pop(new_list.index(self.GetLastClickedOn()))
            self.CanvasObjects = new_list
            
            self.ResetLastClickedOn()
            self.DoDrawing()
    
    def OnPaste(self, event):
        if self.copied:
            self.CanvasObjects.append(self.copied)
            self.copied = None
            self.ResetLastClickedOn()
            self.DoDrawing()
    
    def OnLeaveWindow(self, event):
        self.DoDrawing()  # Repaint everything to simiply fix everything for now
    
    def OnMouseLeftDown(self, event):
        # Call parent method first
        
        m_pos = event.GetPosition()
        
        if self.tool:
            if self.tool == TOOL_PLACE_SQUARE:
                self.AddCanvasObject(Square(self, m_pos, self.color, (30, 30)))
                self.ResetLastClickedOn()
                
            elif self.tool == TOOL_PLACE_TRIANGLE:
                self.AddCanvasObject(Triangle(self, m_pos, self.color, (30, 30)))
                self.ResetLastClickedOn()
            
            # Interaction Tools
            elif self.tool == TOOL_LINK:
                if self.LastClickedOn and self.GetBelowMouse(event):
                    self.LastClickedOn.AddLink(self.GetBelowMouse(event))
                    self.ResetLastClickedOn()
                elif self.GetBelowMouse(event):
                    self.LastClickedOn = self.GetBelowMouse(event)
        
        elif self.tool == None:
            self.holdingBox = self.GetBelowMouse(event, True)
            
            self.parent.RightPanel.tab1.CleanSlate()
            self.parent.RightPanel.tab2.CleanSlate()
            
            if self.holdingBox:
                
                self.LastClickedOn = self.holdingBox # This helps keep track of what we want to alter
                
                # Display the attributes in the area
                self.x_offset = self.holdingBox.GetX() - m_pos.x
                self.y_offset = self.holdingBox.GetY() - m_pos.y
                self.parent.RightPanel.tab1.RedrawDisplay()
                self.parent.RightPanel.tab2.RedrawDisplay()
            else:
                self.ResetLastClickedOn()
    
    def OnMouseLeftUp(self, event):
        m_pos = event.GetPosition()
        
        if self.holdingBox and self.GetGroups():
            xy_pos = 0
            compare_side = m_pos.x # Assume the groups are not flipped at first to reduce the condition checks
            width = self.GetSize()[0]
            portion = width / len(self.GetGroups())
            
            if self.GetFlippedGroups(): # If the groups are flipped then compare from the other side
                compare_side = m_pos.y
            
            for lane in self.GetGroups():
                if compare_side > xy_pos and compare_side < (xy_pos + portion):
                    self.holdingBox.SetGroup(lane)
                
                xy_pos += portion
        
        if self.tool == None and self.holdingBox != None:
            new_pos = self.GetPointWithinCanvas(m_pos.x + self.x_offset, m_pos.y + self.y_offset)
            
            self.holdingBox.SetPosition( new_pos )
            self.CanvasObjects.append( self.holdingBox )
            self.holdingBox = None
    
    def OnMouseRightDown(self, event):
        self.tool = None
        self.color = None
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
    
    def OnMouseMotion(self, event):
        m_pos = event.GetPosition()
        if self.holdingBox:
            new_pos = self.GetPointWithinCanvas(m_pos.x + self.x_offset, m_pos.y + self.y_offset)
            
            self.holdingBox.SetPosition( new_pos )
        
        if self.tool == None:
            if self.GetBelowMouse(event):
                self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            else:
                self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        
        self.DoDrawing(event)
    
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.DoDrawing(event, dc)
    
    def RandomRGBHexString(self, length = 6):
        return str().join([randint(0,15).__hex__()[-1] for item in range(length)]) # return the last character in the string which is the hex value

    def RemoveVariable(self, var):
        # This is a caused by a cascade when removing a variable out of the canvas' scope
        # This removes the variable from all tasks that contain it.
        for obj in self.GetObjects():
            if var in obj.GetVariables():
                obj.RemoveVariable(var)
    
    def ResetLastClickedOn(self):
        self.LastClickedOn = None
        self.parent.RightPanel.tab1.CleanSlate()
        self.parent.RightPanel.tab2.CleanSlate()
    
    def SortLinear(self):
        def NextLink(node, x_pos, y_pos, lanes):
            
            node.SetPosition(x_pos, y_pos)
            
            for group in node.GetObjectLinks():
                if lanes.Get(group.GetGroup()):
                    x1, x2 = lanes.Get(group.GetGroup())
                    half_x = (x1 + x2) / 2
                    spacing = 0
                    if len(node.GetObjectLinks()) > 1:
                        spacing = float(lanes['portion']) / (len(node.GetObjectLinks()) * 2)
                        
                    n = node.GetObjectLinks().index(group) + 1
                    NextLink(group, half_x + (math.pow(-1, n) * (spacing / 2) * n), y_pos + 50, lanes)
                
                else:
                    # This holds the same group as the previous node, such as a task to decision relationship or task to end_state
                    NextLink(group, x_pos + (lanes['portion'] / 2 / len(node.GetObjectLinks()) + 1) * node.GetObjectLinks().index(group), y_pos + 50, lanes)
        
        lanes = {}
        last_lane = None
        lanes['portion'] = self.GetSize()[0] / 2
        
        if self.GetGroups():
            x_pos = 0
            width = self.GetSize()[0]
            portion = width / len(self.GetGroups())
            
            lanes['portion'] = portion
            
            for lane in self.GetGroups():
                lanes[lane] = (x_pos, x_pos + portion)
                x_pos += portion
        
        x_pos = lanes['portion'] / 2
        y_pos = 100
        if self.CanvasObjects != []:
            fnode = self.CanvasObjects[0]
            
            # Recurrsivally travel through the build and work out everything
            NextLink(fnode, x_pos, y_pos, lanes)
            self.DoDrawing()
    
    def UpdateAllInteractables(self):
        for ele in self.GetObjects():
            ele.RefreshLinks()
