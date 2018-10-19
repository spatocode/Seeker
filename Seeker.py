#!/usr/bin/python3
# -*- coding: utf-8 -*-

import wx
from utils.common import scale_image

class Seeker(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Seeker, self).__init__(*args, **kwargs)
        self.InitUI()


    def InitUI(self):
        self.Center()
        self.createMenuBar()
        self.createToolAndTab()

    
    def createToolAndTab(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        choices = [
            "Local Area Connection* 3", 
            "Local Area Connection* 4", 
            "Wi-Fi 3", 
            "Ethernet", 
            "Ethernet 4", 
            "Npcap Loopback Adapter", 
            "Ethernet 3", 
            "Wi-Fi 2", 
            "Loopback"
        ]

        self.toolbar1 = wx.ToolBar(self)
        adapterList = wx.Choice(self.toolbar1, wx.ID_ANY, choices=choices)
        adapterList.SetSelection(0)
        startCaptureTool = self.toolbar1.AddTool(1, "Capture packets", scale_image("assets/start_capture.png"), "Capture packets")
        stopCaptureTool = self.toolbar1.AddTool(2, "Stop Capture", scale_image("assets/stop_capture.png"), "Stop capture")
        
        self.toolbar1.EnableTool(2, False)
        self.toolbar1.AddSeparator()
        self.toolbar1.AddControl(adapterList)
        self.toolbar1.AddSeparator()
        
        startScanTool = self.toolbar1.AddTool(3, "Scan", scale_image("assets/play.png"), "Scan for computers on the network")
        stopScan = self.toolbar1.AddTool(4, "Stop", scale_image("assets/stop.png"), "Stop scan")
        self.toolbar1.EnableTool(4, False)
        addComputerTool = self.toolbar1.AddTool(wx.ID_ANY, "Add computer", scale_image("assets/add_computer.png"), "Add computer")
        self.toolbar1.AddSeparator()
        self.toolbar1.Realize()

        """statMenu = wx.Menu()
        statMenu.Append(wx.ID_ANY, "IP Connection Statistics")
        statMenu.Append(wx.ID_ANY, "Packets Data Statistics")
        statMenu.Append(wx.ID_ANY, "VoIP Statistics")

        saveMenu = wx.Menu()
        saveMenu.Append(wx.ID_ANY, "Save IP Connections Data")
        saveMenu.Append(wx.ID_ANY, "Save Packets Data")
        saveMenu.Append(wx.ID_ANY, "Save VoIP Data")

        clearMenu = wx.Menu()
        clearMenu.Append(wx.ID_ANY, "Clear IP Connections Data")
        clearMenu.Append(wx.ID_ANY, "Clear Packets Data")
        clearMenu.Append(wx.ID_ANY, "Clear VoIP Data")
        clearMenu.Append(wx.ID_ANY, "Clear Saved Computers")
        clearMenu.Append(wx.ID_ANY, "Clear All Tabs")"""

        self.toolbar2 = wx.ToolBar(self)
        self.toolbar2.AddTool(5, "Statistics", scale_image("assets/stats.png"), "Statistics")
        #self.toolbar2.SetDropdownMenu(5, statMenu)
        
        self.toolbar2.AddTool(6, "Save", scale_image("assets/save.png"), "Save")
        #self.toolbar2.SetDropdownMenu(6, saveMenu)

        self.toolbar2.AddTool(7, "Clear", scale_image("assets/clear.png"), "Clear")
        #self.toolbar2.SetDropdownMenu(7, saveMenu)

        self.toolbar2.AddTool(wx.ID_ANY, "Find", scale_image("assets/find.png"), "Find")
        self.toolbar2.AddTool(wx.ID_ANY, "Options", scale_image("assets/options.png"), "Options")
        self.toolbar2.Realize()

        vbox.Add(self.toolbar1, 0, wx.EXPAND)
        vbox.Add(self.toolbar2, 0, wx.EXPAND)
        self.SetSizer(vbox)


    def createMenuBar(self):
        fileMenu = wx.Menu()
        captureItem = fileMenu.Append(wx.ID_ANY, "&Capture Packets")
        ipScanItem = fileMenu.Append(wx.ID_ANY, "&Scan IP")
        addComputerItem = fileMenu.Append(wx.ID_ANY, "&Add Computer")
        clearSavedComputerItem = fileMenu.Append(wx.ID_ANY, "&Clear Saved Computers")
        clearLatestIPItem = fileMenu.Append(wx.ID_ANY, "&Clear Latest IP Connections")
        clearPacketsItem = fileMenu.Append(wx.ID_ANY, "&Clear Packets")
        clearVoIPItem = fileMenu.Append(wx.ID_ANY, "&Clear VoIP")
        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        issueItem = helpMenu.Append(wx.ID_ANY, "&Report Issue")
        tutorialItem = helpMenu.Append(wx.ID_ANY, "&Online Tutorial")
        updateItem = helpMenu.Append(wx.ID_ANY, "&Check for updates...")
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        languages = wx.Menu()
        languages.Append(wx.ID_ANY, "English")
        languages.Append(wx.ID_ANY, "French")
        languages.Append(wx.ID_ANY, "Spanish")
        languages.Append(wx.ID_ANY, "German")
        languages.Append(wx.ID_ANY, "Japanese")
        languages.Append(wx.ID_ANY, "Russian")
        languages.Append(wx.ID_ANY, "Chinese")

        settingsMenu = wx.Menu()
        optionsItem = settingsMenu.Append(wx.ID_ANY, "&Options")
        settingsMenu.AppendMenu(wx.ID_ANY, "&Language", languages)

        viewMenu = wx.Menu()
        self.showToolbarItem = viewMenu.Append(wx.ID_ANY, "Show toolbar", "Show Toolbar", kind=wx.ITEM_CHECK)
        statisticsItem = viewMenu.Append(wx.ID_ANY, "&Statistics")
        viewMenu.Check(self.showToolbarItem.GetId(), True)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(viewMenu, "&View")
        menuBar.Append(settingsMenu, "&Settings")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)


if __name__ == "__main__":
    app = wx.App()
    window = Seeker(None, title="Seeker", size=(1000, 600))
    window.Show()
    app.MainLoop()
