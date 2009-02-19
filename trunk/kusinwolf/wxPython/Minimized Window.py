#!/usr/bin/python

import wx

app = wx.App()

frame = wx.Frame(None, title="Minimized Window", style=wx.MAXIMIZE_BOX |
                 wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
frame.Show(True)

app.MainLoop()
