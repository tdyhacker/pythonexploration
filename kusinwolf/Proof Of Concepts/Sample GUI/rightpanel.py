from globals import *
from classes import *

################################
# Right Pannel With Attributes #
################################

class RightPanel(wx.Panel):
    def __init__(self, parent, id):
        '''
            RightPanel(Frame parent, Int id, Tuple tabs)
        '''
        wx.Panel.__init__(self, parent, id)
        
        self.tab_number = 1
        
        self.parent = parent
        self.CanvasName = "Canvas"
        
        #self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        #self.Bind(wx.EVT_KEY_UP, self.OnKeyDown)
    
    def AddTab(self, tab):
        self.__setattr__('tab%s' % self.tab_number, tab)
        self.tab_number += 1
    
    def AddVariable(self, var):
        self.parent.AddVariable(var)
    
    def GetLastClickedOn(self):
        return self.parent.GetLastClickedOn()
    
    def GetGroups(self):
        return self.parent.GetGroups()
    
    def GetVariables(self):
        return self.parent.GetVariables()
    
    def OnButtonClick(self, event): 
        button = event.GetEventObject()
        button_id = button.GetId()
        
        if button_id == 1:
            pass
        elif button_id == 2: # Add new variable to task
            var = self.tab2.GetNewVariable()
            self.GetLastClickedOn().AddVariable(var)
            
            self.tab2.RedrawDisplay()
        
        elif button_id == 3: # Add new group
            #list = self.GetGroups()
            self.GetGroups().append(self.tab3.GetNewGroup())
            self.GetGroups().sort()
            #self.parent.SetGroups(list)
            self.UpdateAllTabs()
            self.parent.Canvas.DoDrawing()
        
        elif button_id == 4: # Swap Overview view
            if self.tab3.new_var_show:
                self.tab3.new_var_show = False # Create a Variable
                self.AddVariable(self.tab2.GetCreatingVariable())
            else:
                self.tab3.new_var_show = True
            self.tab3.RedrawDisplay()
        
        elif button_id == 5: # Close Overview swapped view
            self.tab3.new_var_show = False
            self.tab3.RedrawDisplay()
        
        elif button_id == 6: # Add all variables
            for var in self.GetVariables():
                if not self.GetLastClickedOn().HasVariable(var):
                    self.GetLastClickedOn().AddVariable(var)
            
            self.tab2.RedrawDisplay()
        
        elif button_id == 7: # Add new variable
            var = self.tab3.GetCreatingVariable()
            self.AddVariable(var)
            
            self.tab3.RedrawDisplay()
        
        elif button_id >= 10 and button_id < 50:
            if self.tab3.new_var_show:
                self.RemoveVariable(self.GetVariables()[button_id - 10])
                self.tab3.RedrawDisplay()
                self.tab2.RedrawDisplay() # Incase the task is still selected and requires updating
            else:
                #list = self.GetGroups()
                self.GetGroups().pop(button_id - 10)
                #self.parent.SetGroups(list)
                self.UpdateAllTabs()
                self.parent.Canvas.DoDrawing()
        
        elif button_id >= 50 and button_id < 100:
            self.GetLastClickedOn().RemoveVariable(self.GetLastClickedOn().GetVariables()[button_id - 50])
            self.tab2.RedrawDisplay()
        
        elif button_id >= 100 and button_id < 150:
            self.GetLastClickedOn().RemoveLink(self.GetLastClickedOn().GetObjectLinks()[button_id - 100])
            self.tab1.RedrawDisplay()
            self.parent.Canvas.DoDrawing()
    
    def OnComboBoxSelect(self, event):
        self.parent.Canvas.GetLastClickedOn().UpdateSelf(**self.tab1.GetAllFieldValues())
    
    def OnKeyUp(self, event):
        # Save Changes made in the text boxes to the objects out on the canvas
        pressed = event.GetKeyCode()
        
        self.parent.Canvas.UpdateAllInteractables() # Refresh every transition
        
        if (pressed >= 44 and pressed <= 96) or pressed == 8 or pressed == 32 or pressed == 39 or pressed == 127: # Letters + Space + Backspace
            if self.parent.Canvas.GetLastClickedOn():
                self.parent.Canvas.GetLastClickedOn().UpdateSelf(**self.tab1.GetAllFieldValues())
                self.parent.Canvas.GetLastClickedOn().UpdateSelf(self.tab2.GetAllFieldValues())
            
            #self.UpdateGroups(self.tab2.GetAllFieldValues())
            self.CanvasName = self.tab3.GetNewCanvasName() or self.CanvasName # In case of None returned
            
            # Redraw last
            self.parent.Canvas.DoDrawing()
    
    def RemoveVariable(self, var):
        self.parent.RemoveVariable(var)
    
    def SetVariables(self, vars):
        self.parent.SetVariables(vars)
    
    def UpdateAllTabs(self):
        #for num in range(1, self.tab_number):
        #    self.__getattribute__("tab%s" % num).RedrawDisplay(obj = None)
        self.tab1.RedrawDisplay()
        self.tab2.RedrawDisplay()
        self.tab3.RedrawDisplay()
    
    def UpdateGroups(self, values):
        if values != []:
            #list = self.GetGroups()
            for row in range(len(values)):
                self.GetGroups()[row] = values[row]
            #self.parent.SetGroups(list)
            self.parent.Canvas.DoDrawing()
    
class Page1(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent)
        
        self.parent = self.GetParent().GetParent() # The visual Parent is the Right panel
        
        self.list_of_text = []
        self.list_of_boxes = []
        self.list_of_buttons = []
        
        self.NameField = None
        self.DescriptionField = None
        self.GroupField = None
        
        self.Bind(wx.EVT_KEY_UP, self.parent.OnKeyUp)
        self.Bind(wx.EVT_COMBOBOX, self.parent.OnComboBoxSelect)
    
    def CleanSlate(self):
        temp = self.list_of_boxes[:] + self.list_of_buttons[:] + self.list_of_text[:]
        
        self.list_of_text = []
        self.list_of_boxes = []
        self.list_of_buttons = []
        
        for item in temp:
            item.Destroy()
        
        if self.NameField:
            self.NameField.Destroy()
            
        if self.DescriptionField:
            self.DescriptionField.Destroy()
            
        if self.GroupField:
            self.GroupField.Destroy()
        
        self.SetScrollbars(10, 10, 0, 0) # Keeps from drawing a funky looking window
    
    def RedrawDisplay(self):
        self.CleanSlate()
        
        renderObject = self.parent.GetLastClickedOn()
        
        y_pos = 0
        tran_delete_button_pos = 100
        
        if renderObject:
            # Interactable Type
            y_pos += 5
            self.list_of_text.append( wx.StaticText(self, -1, renderObject.GetType().replace("_", ' ').capitalize(), pos = (5, y_pos)) )
            
            # Task Name
            y_pos += 30
            self.list_of_text.append( wx.StaticText(self, -1, "Name", pos = (5, y_pos)) )
            y_pos += 20
            self.NameField = wx.TextCtrl(self, 1, pos = (5, y_pos), size = (200, 25))
            self.NameField.SetValue(renderObject.GetName())
            
            # Task Description
            y_pos += 30
            self.list_of_text.append( wx.StaticText(self, -1, "Description", pos = (5, y_pos)) )
            y_pos += 20
            self.DescriptionField = wx.TextCtrl(self, 1, pos = (5, y_pos), size = (200, 25))
            self.DescriptionField.SetValue(renderObject.GetDescription())
            
            # Task Group
            #y_pos += 30
            #self.list_of_text.append( wx.StaticText(self, -1, "Group", pos = (5, y_pos)) )
            #y_pos += 20
            ##self.GroupField = wx.TextCtrl(self, 1, pos = (5, y_pos), size = (200, 25))
            #self.GroupField = wx.ComboBox(self, 1, pos = (5, y_pos), size = (200, 25), choices = self.parent.GetGroups())
            #self.GroupField.SetValue(renderObject.GetGroup())
            
            for tran in range(len(renderObject.GetObjectLinks())):
                y_pos += 30
                
                # Links To
                self.list_of_text.append( wx.StaticText(self, -1, "Links To", pos = (5, y_pos)) )
                
                y_pos += 20
                
                del_button = wx.Button(self, tran_delete_button_pos, 'X', pos = (5, y_pos), size = (25, 25))
                self.list_of_buttons.append(del_button)
                
                y_pos += 5
                self.Bind(wx.EVT_BUTTON, self.parent.OnButtonClick, id = tran_delete_button_pos) # Not sure if this has to be with the button recreation or not
                tran_delete_button_pos += 1
                y_pos -= 5
                
                text = wx.StaticText(self, -1, renderObject.GetObjectLinks()[tran].GetName(), pos = (35, y_pos))
                self.list_of_text.append(text)
                
                if self.parent.parent.InViewAdvanced():
                    y_pos += 25
                    textbox = wx.TextCtrl(self, -1, pos = (5, y_pos), size = (200, 25))
                    self.list_of_boxes.append(textbox)
                    textbox.SetValue(str(compile(".*#{(.*)}.*").match(renderObject.GetLinks()[tran].condition[0].valueOf_.replace("\n", '')).group(1)))
                
            y_pos += 25
        
        self.SetScrollbars(10, 10, 20, (y_pos / 10)) # seems to be perfect length
    
    def OnKeyDown(self, event):
        print event.GetKeyCode()
    
    def GetAllFieldValues(self):
        return {"task_name": str(self.NameField.GetValue()),
                "description": str(self.DescriptionField.GetValue()),
                #"group": str(self.GroupField.GetValue())
                }

class Page2(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent)
        
        self.SetScrollbars(10, 10, 20, 100)
        
        self.parent = self.GetParent().GetParent() # The visual Parent is the Right panel
        
        text = wx.StaticText(self, -1, "Interactable Variable List", pos = (5,5))
        
        self.list_of_text = [text,]
        self.list_of_boxes = []
        self.list_of_buttons = []
        self.new_variable = None
        
        self.Bind(wx.EVT_KEY_UP, self.parent.OnKeyUp)
        
        # Not sure if these have to be with the button recreation or not, but it doesn't seem like it
        self.Bind(wx.EVT_BUTTON, self.parent.OnButtonClick, id=2)
        self.Bind(wx.EVT_BUTTON, self.parent.OnButtonClick, id=4)
        self.Bind(wx.EVT_BUTTON, self.parent.OnButtonClick, id=6)
    
    def CleanSlate(self):
        temp = self.list_of_boxes[:] + self.list_of_buttons[:] + self.list_of_text[:]
        
        self.list_of_text = []
        self.list_of_boxes = []
        self.list_of_buttons = []
        
        self.SetScrollbars(10, 10, 0, 0) # Keeps from drawing a funky looking window
        
        for item in temp:
            item.Destroy()
        
        if self.new_variable:
            self.new_variable.Destroy()
            
        text = wx.StaticText(self, -1, "Interactable Variable List", pos = (5, 5))
        self.list_of_text.append(text)
    
    def RedrawDisplay(self):
        self.CleanSlate()
        
        renderObject = self.parent.GetLastClickedOn()
        y_pos = 0
        
        if renderObject:
            y_pos = 25 # Physical position on the GUI
            var_delete_button_pos = 50 # Logical position in the list
            
            y_pos += 30
            self.list_of_text.append( wx.StaticText(self, -1, "Variables", pos = (5, y_pos)) )
            y_pos += 20
            #self.GroupField = wx.TextCtrl(self, 1, pos = (5, y_pos), size = (200, 25))
            self.new_variable = wx.ComboBox(self, 1, pos = (5, y_pos), size = (200, 25), choices = [var for var in self.parent.GetVariables() if not renderObject.HasVariable(var)])
            
            y_pos += 30
            
            add_button = wx.Button(self, 6, 'Add All', pos = (105, y_pos), size = (-1, 25))
            self.list_of_buttons.append(add_button)
            
            add_button = wx.Button(self, 2, 'Add Variable', pos = (5, y_pos), size = (-1, 25))
            self.list_of_buttons.append(add_button)
            
            y_pos += 40
            
            for var in renderObject.GetVariables():
                y_pos += 5
                
                del_button = wx.Button(self, var_delete_button_pos, 'X', pos = (5, y_pos), size = (25, 25))
                self.list_of_buttons.append(del_button)
                
                y_pos += 5
                self.Bind(wx.EVT_BUTTON, self.parent.OnButtonClick, id = var_delete_button_pos) # Not sure if this has to be with the button recreation or not
                var_delete_button_pos += 1
                
                text = wx.StaticText(self, -1, var, pos = (35, y_pos))
                self.list_of_text.append(text)
                
                y_pos += 25
            
            y_pos += 25
        
        self.SetScrollbars(10, 10, 20, (y_pos / 10)) # seems to be perfect length
    
    def GetAllFieldValues(self):
        return [field.GetValue() for field in self.list_of_boxes]
    
    def GetNewVariable(self):
        for var in self.parent.GetVariables():
            if var == str(self.new_variable.GetValue()):
                return var
        
        return None

class Page3(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent)
        
        self.parent = self.GetParent().GetParent() # The visual Parent is the Right panel
        
        self.list_of_text = []
        self.list_of_boxes = []
        self.list_of_buttons = []
        self.new_group_name = None
        self.new_variable_name = None
        self.new_var_show = False
        self.canvas_name = None
        
        self.RedrawDisplay()
        
        self.Bind(wx.EVT_KEY_UP, self.parent.OnKeyUp)
        
        # Not sure if these have to be with the button recreation or not, but it doesn't seem like it
        self.Bind(wx.EVT_BUTTON, self.parent.OnButtonClick, id=3)
        self.Bind(wx.EVT_BUTTON, self.parent.OnButtonClick, id=4)
        self.Bind(wx.EVT_BUTTON, self.parent.OnButtonClick, id=5)
        self.Bind(wx.EVT_BUTTON, self.parent.OnButtonClick, id=7)
    
    def CleanSlate(self):
        temp = self.list_of_boxes[:] + self.list_of_buttons[:] + self.list_of_text[:]
        
        self.list_of_text = []
        self.list_of_boxes = []
        self.list_of_buttons = []
        
        self.SetScrollbars(10, 10, 0, 0) # Keeps from drawing a funky looking window
        
        if self.new_variable_name:
            self.new_variable_name.Destroy()
            
        if self.canvas_name:
            self.canvas_name.Destroy()
        if self.new_group_name:
            self.new_group_name.Destroy()
            
        for item in temp:
            item.Destroy()
        
    
    def RedrawDisplay(self):
        self.CleanSlate()
        
        y_pos = 0 # Physical position on the GUI
        var_delete_button_pos = 10 # Logical position in the list
        
        y_pos += 5
        text = wx.StaticText(self, -1, "Canvas", pos = (5, y_pos))
        self.list_of_text.append(text)
        
        if self.new_var_show:
            # Adding variables to interactables
            y_pos += 30
            text = wx.StaticText(self, -1, "New Variable Name", pos = (5, y_pos))
            self.list_of_text.append(text)
            
            y_pos += 25
            self.new_variable_name = wx.TextCtrl(self, -1, pos = (5, y_pos), size = (200, 25))
            
            y_pos += 30
            add_button = wx.Button(self, 7, 'Add Variable', pos = (5, y_pos), size = (-1, 25))
            self.list_of_buttons.append(add_button)
            
            add_button = wx.Button(self, 5, 'Close', pos = (105, y_pos), size = (-1, 25))
            self.list_of_buttons.append(add_button)
            
            y_pos += 35
            for var in self.parent.GetVariables():
                y_pos += 5
                
                del_button = wx.Button(self, var_delete_button_pos, 'X', pos = (5, y_pos), size = (25, 25))
                self.list_of_buttons.append(del_button)
                
                y_pos += 5
                self.Bind(wx.EVT_BUTTON, self.parent.OnButtonClick, id = var_delete_button_pos) # Not sure if this has to be with the button recreation or not
                var_delete_button_pos += 1
                
                text = wx.StaticText(self, -1, var, pos = (35, y_pos))
                self.list_of_text.append(text)
                
                y_pos += 25
            
            y_pos += 25
        
        else:
            y_pos += 25
            self.canvas_name = wx.TextCtrl(self, -1, pos = (5, y_pos), size = (200, 25))
            self.canvas_name.SetValue(self.parent.CanvasName)
            
            y_pos += 30
            add_button = wx.Button(self, 4, 'Create/Edit Variables', pos = (5, y_pos), size = (-1, 25))
            self.list_of_buttons.append(add_button)
            
            # New Group
            y_pos += 30
            text = wx.StaticText(self, -1, "New Group", pos = (5, y_pos))
            self.list_of_text.append(text)
            
            y_pos += 25
            self.new_group_name = wx.TextCtrl(self, -1, pos = (5, y_pos), size = (200, -1))
            
            y_pos += 30
            add_button = wx.Button(self, 3, 'Add Group', pos = (5, y_pos), size = (-1, 25))
            self.list_of_buttons.append(add_button)
        
            y_pos += 40        
            for lane in self.parent.GetGroups():
                y_pos += 5
                del_button = wx.Button(self, var_delete_button_pos, 'X', pos = (5, y_pos), size = (25, 25))
                self.list_of_buttons.append(del_button)
                self.Bind(wx.EVT_BUTTON, self.parent.OnButtonClick, id = var_delete_button_pos) # Not sure if this has to be with the button recreation or not
                var_delete_button_pos += 1
                
                y_pos += 5
                text = wx.StaticText(self, -1, lane, pos = (35, y_pos))
                self.list_of_text.append(text)            
                y_pos += 25
        
        self.SetScrollbars(10, 10, 20, (y_pos / 10)) # seems to be perfect length
    
    def GetAllFieldValues(self):
        return [field.GetValue() for field in self.list_of_boxes]
    
    def GetCreatingVariable(self):
        return str(self.new_variable_name.GetValue())
    
    def GetNewGroup(self):
        return str(self.new_group_name.GetValue())
    
    def GetNewCanvasName(self):
        if self.canvas_name:
            return str(self.canvas_name.GetValue())
        else:
            return None
    