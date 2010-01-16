# Required modules from python
import wx
from wx.lib import ogl
from random import randint
import math
from shutil import copyfile
from re import compile
import copy

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
MENU_ID_ADVANCEDVIEW = itterID()
MENU_ID_CLEAR_CANVAS = itterID()
MENU_ID_EXIT = itterID()
MENU_ID_FLIP_GROUPS = itterID()
MENU_ID_LOAD = itterID()
MENU_ID_NEW = itterID()
MENU_ID_SAVE = itterID()
MENU_ID_SAVEAS = itterID()
MENU_ID_SAVE_IMAGE = itterID()
MENU_ID_SIMPLEVIEW = itterID()
MENU_ID_SORT_LINEAR = itterID()

MENU_DEBUG_MODE = itterID()

MENU_COPY_INTERACTABLE = itterID()
MENU_PASTE_INTERACTABLE = itterID()
MENU_DELETE_INTERACTABLE = itterID()

# ID's for tools clicked on
TOOL_PLACE_SQUARE = itterID()
TOOL_PLACE_TRIANGLE = itterID()
TOOL_LINK = itterID()