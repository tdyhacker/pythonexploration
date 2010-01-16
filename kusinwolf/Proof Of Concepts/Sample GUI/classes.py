from globals import *

#####################
# Paintable Objects #
#####################

# This class helps keep track of altering anything on the screen  of interest that can be altered throughout the session
class Interactable(object):
    def __init__(self, canvas, point, color, size, name = ""):
        # Set the place
        self.SetX(point.x)
        self.SetY(point.y)
        
        self.SetSize(size[0], size[1])
        
        self.id = objItterID()
        self.color = color
        #self.canvas = canvas
        self.objLinks = []
        self.group = None
        self.variables = []
        self.name = name
        
        self.type = "Interactable"
        self.description = ""
        
        ## Test data
        #if self.variables == []:
        #    self.AddVariable(Variable(name = "Bob1"))
        #    self.AddVariable(Variable(name = "Bob2"))
        #    self.AddVariable(Variable(name = "Bob3"))
        #    self.AddVariable(Variable(name = "Bob4"))
    
    def __repr__(self):
        return self.GetName()

    def AddLink(self, tran):
        self.SetObjectLinks( self.GetObjectLinks() + [tran,] )
    
    def AddVariable(self, var):
        if var != '' and var != None and not self.HasVariable(var):
            self.SetVariables(self.GetVariables() + [var,])
    
    def DrawLines(self, surface):
        if self.GetObjectLinks() and type(self.GetObjectLinks()) != list:
            surface.DrawLine(self.GetCenter().x, self.GetCenter().y, self.GetObjectLinks().GetCenter().x, self.GetObjectLinks().GetCenter().y)
        elif self.GetObjectLinks() and type(self.GetObjectLinks()) == list:
            for item in self.GetObjectLinks():
                surface.DrawLine(self.GetCenter().x, self.GetCenter().y, item.GetCenter().x, item.GetCenter().y)
    
    def IsBeneathMouse(self, point):
        return (point.x >= self.GetX() - self.GetWidth() / 2 and point.x <= self.GetX() + self.GetWidth() / 2 and point.y >= self.GetY() - self.GetHeight() / 2 and point.y <= self.GetY() + self.GetHeight() / 2)
    
    def GetCenter(self):
        # Find the Square center of the polygon
        # TODO: I will calculate the absolute center later
        if self.GetX() and self.GetY():
            return wx.Point(self.GetX(), self.GetY())
        else:
            return wx.Point(0, 0) # There is no center
    
    def GetCopy(self):
        # If the canvas is not removed during a copy, it will be attempted to be copied,
        # in essience a duplicate version of the entire program will be created which is
        # equivalent to dividing by zero :)
        
        # Hide anything
        
        # If I don't do this, then an invisible block is hiding in memory outside of the canvas' reach
        hide = self.objLinks 
        self.objLinks = None
        # Copy
        new_copy = copy.deepcopy(self) # This automatically copies everything
        new_copy.SetName("Copy of: %s" % new_copy.GetName())
        # Reassign everything
        new_copy.objLinks = hide
        self.objLinks = hide
        
        return new_copy
    
    def GetHeight(self):
        return self.size_y
    
    def GetObjectLinks(self):
        return self.objLinks
    
    def GetLinks(self):
        return self.GetObjectLinks()
    
    def GetDescription(self):
        return self.description
    
    def GetGroup(self):
        return self.group
    
    def GetName(self):
        return self.name
    
    def GetType(self):
        return self.type
    
    def GetVariables(self):
        return self.variables

    def GetWidth(self):
        return self.size_x
    
    def GetX(self):
        return self.x
    
    def GetY(self):
        return self.y
    
    def HasVariable(self, var):
        for cvar in self.GetVariables():
            if cvar == var:
                return True
        
        return False
    
    def RefreshLinks(self):
        self.SetLinks([])
        for tran in self.GetObjectLinks():
            self.SetLinks( self.GetLinks() + [tran,] )
    
    def RemoveLink(self, tran):
        # Need to remove the link interactable and link object
        this_elm = None
        
        # Remove link object
        new_list = self.GetObjectLinks()
        new_list.pop(self.GetObjectLinks().index(tran))
        self.SetObjectLinks(new_list)
        
        # Find link interactable
        if type(self.GetLinks()) == list:
            for tran_elm in self.GetLinks():
                if str(tran_elm.to) == tran.GetName():
                    this_elm = tran_elm
            
            # Remove link interactable
            new_list = self.GetLinks()
            new_list.pop(self.GetLinks().index(this_elm))
            self.SetLinks(new_list)
        else:
            # Remove link interactable
            self.SetLinks(None)
    
    def RemoveVariable(self, var):
        found = False
        
        for cvar in self.GetVariables():
            if cvar == var:
                found = True
        
        if found:
            new_list = self.GetVariables()
            new_list.pop(new_list.index(var))
            self.SetVariables(new_list)
    
    def RebuildVertices(self, scaler_fn = None):
        self.vertices = [] # Clear them out
        
        scaler_fn = scaler_fn or (lambda x : int((x / 2.0)))
        
        # Upper Left
        self.vertices.append(wx.Point(x = ( self.x - scaler_fn( self.size_x ) ),
                                      y = ( self.y - scaler_fn( self.size_y ) ) ))
        
        # Lower Left
        self.vertices.append(wx.Point(x = ( self.x - scaler_fn( self.size_x ) ),
                                      y = ( self.y + scaler_fn( self.size_y ) ) ))
        
        # Lower Right
        self.vertices.append(wx.Point(x = ( self.x + scaler_fn( self.size_x ) ),
                                      y = ( self.y + scaler_fn( self.size_y ) ) ))
        
        # Upper Right
        self.vertices.append(wx.Point(x = ( self.x + scaler_fn( self.size_x ) ),
                                      y = ( self.y - scaler_fn( self.size_y ) ) ))
        
        # Also reassign the boundaries
        self.SetBoundaries()
    
    def Render(self, dc):
        dc.SetPen(wx.Pen('#000000', width = 0, style = wx.TRANSPARENT))
        dc.SetBrush(wx.Brush(self.color))
        dc.DrawPolygon(self.vertices)
        dc.DrawText(self.GetName(), self.x - (len(self.GetName()) / 2) * 8, self.y - 10) # Display the task name
    
    def Save(self):
        return "%s, %s" % (self.GetCenter(), self.GetName())
        
    def SetBoundaries(self):
        if self.vertices:
            LeftX = RightX = self.vertices[0].x
            TopY = BottomY = self.vertices[0].y
            for point in self.vertices:
                if point.x < LeftX:
                    LeftX = point.x
                elif point.x > RightX:
                    RightX = point.x
                
                if point.y < TopY:
                    TopY = point.y
                elif point.y > BottomY:
                    BottomY = point.y
                
            # Tuples of the bounding boxes
            self.bounding_x = (LeftX, RightX)
            self.bounding_y = (TopY, BottomY)
            
            # Almost no need for this code now
            # If the values are not in least to greatest order, then IsBeneathMouse would always return false
            #self.bounding_x = list(self.bounding_x)
            #self.bounding_x.sort()
            #self.bounding_x = tuple(self.bounding_x)
            #
            #self.bounding_y = list(self.bounding_y)
            #self.bounding_y.sort()
            #self.bounding_y = tuple(self.bounding_y)
    
    def SetHeight(self, y):
        self.size_y = y
    
    def SetObjectLinks(self, item):
        self.objLinks = item
    
    def SetLinks(self, item):
        self.SetObjectLinks(item)
    
    def SetPosition(self, x, y = None):
        if type(x) == wx.Point:
            self.SetX(x.x)
            self.SetY(x.y)
        elif type(x) != wx.Point and y == None:
            print "ERROR: Wrong Point Type"
        elif x and y:
            self.SetX(x)
            self.SetY(y)
        
        self.RebuildVertices()
    
    def SetSize(self, x, y):
        ''' Sets up a rectangle by default'''
        self.SetWidth(x)
        self.SetHeight(y)
        
        self.RebuildVertices()
    
    def SetDescription(self, description):
        self.description = description
    
    def SetGroup(self, group):
        self.group = group
    
    def SetName(self, name):
        self.name = name
    
    def SetVariables(self, vars):
        self.variables = vars
    
    def SetWidth(self, x):
        self.size_x = x
    
    def SetX(self, x):
        self.x = x
    
    def SetY(self, y):
        self.y = y
    
    def UpdateSelf(self, list_of_fields = None, **kwgs):
        if list_of_fields:
            for row in range(len(list_of_fields)):
                self.GetVariables()[row] = list_of_fields[row]
        
        if kwgs.get("_name") == "":
            self.SetName(kwgs.get("name"))
        else:
            self.SetName(kwgs.get("name") or self.GetName())
        
        if kwgs.get("description") == "":
            self.SetDescription(kwgs.get("description"))
        else:
            self.SetDescription(kwgs.get("description") or self.GetDescription())
        
        if kwgs.get("group") == "":
            self.SetGroup(kwgs.get("group"))
        else:
            self.SetGroup(kwgs.get("group") or self.GetGroup())

class Square(Interactable):
    type = "Square"

class Triangle(Interactable):
    type = "Triangle"
    
    def RebuildVertices(self, scaler_fn = None):
        self.vertices = [] # Clear them out
        
        scaler_fn = scaler_fn or (lambda x : int((x / 1.5)))
        
        # Top Point
        self.vertices.append(wx.Point(x = ( self.x ),
                                      y = ( self.y - scaler_fn( self.size_y ) )
                                      )
                            )
        
        # Left Point
        self.vertices.append(wx.Point(x = ( self.x - scaler_fn( self.size_x ) ),
                                      y = ( self.y )
                                      )
                            )
        
        # Bottom Point
        self.vertices.append(wx.Point(x = ( self.x ),
                                      y = ( self.y + scaler_fn( self.size_y ) )
                                      )
                            )
        
        # Right Point
        self.vertices.append(wx.Point(x = ( self.x + scaler_fn( self.size_x ) ),
                                      y = ( self.y )
                                      )
                            )
        
        # Also reassign the boundaries
        self.SetBoundaries()