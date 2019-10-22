#!/usr/bin/python3
# -*- coding: utf-8 -*-

import wx
import wx.adv
from wx.lib.wordwrap import wordwrap
from wx.lib.pubsub import pub
from sniffer.sniff import SniffThread
from radmin.scan import Scan
from interface.popup import PopupMenu
from interface.tab import NoteBook
from utils.common import scale_image
from setup import *

class Seeker(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Seeker, self).__init__(*args, **kwargs)
        self.InitUI()


    def InitUI(self):
        self.Center()
        self.notebook = NoteBook(self)
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
        vbox.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(vbox)

        self.Bind(wx.EVT_TOOL, self.OnStartCapture, startCaptureTool)
        self.Bind(wx.EVT_TOOL, self.OnStopCapture, stopCaptureTool)
        self.Bind(wx.EVT_TOOL, self.OnAddComputer, addComputerTool)
        self.Bind(wx.EVT_TOOL, self.OnStartScan, startScanTool)


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
        self.Bind(wx.EVT_MENU, self.OnToggleToolbar, self.showToolbarItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnStartCapture, captureItem)
        self.Bind(wx.EVT_MENU, self.OnAddComputer, addComputerItem)
        self.Bind(wx.EVT_MENU, self.OnStartScan, ipScanItem)
        self.Bind(wx.EVT_MENU, self.OnClearSavedComputer, clearSavedComputerItem)
        self.Bind(wx.EVT_MENU, self.OnClearLatestIPConn, clearLatestIPItem)


    def OnAddComputer(self, event):
        self.notebook.SetSelection(1)
        dialog = wx.TextEntryDialog(self, "IP Address", "Add to saved computers", "0.0.0.0")
        
        if dialog.ShowModal() == wx.ID_OK:
            data = ["Dead", "", dialog.GetValue(), "", ""]
            self.notebook.savedComputers.updateDisplay(data)

        dialog.Destroy()


    def OnStartScan(self, event):
        dialog = wx.TextEntryDialog(self, "Enter IP", "Scan IP", "Example: 190.10.212.1 - 193.164.0.3 OR 127.0.0.1")

        if dialog.ShowModal() == wx.ID_OK:
            self.toolbar1.EnableTool(3, False)
            self.toolbar1.EnableTool(4, True)
            self.notebook.SetSelection(0)

            self.scanthread = Scan(dialog.GetValue())

            self.toolbar1.EnableTool(3, True)
            self.toolbar1.EnableTool(4, False)

        dialog.Destroy()


    def OnStopScan(self, event):
        if self.scanthread:
            self.scanthread.stop()
            self.toolbar1.EnableTool(3, True)
            self.toolbar1.EnableTool(4, False)


    def OnClearSavedComputer(self, event):
        self.notebook.savedComputers.listctrl.DeleteAllItems()


    def OnToggleToolbar(self, event):
        if self.showToolbarItem.IsChecked():
            self.toolbar1.Show()
            self.toolbar2.Show()
        else:
            self.toolbar1.Hide()
            self.toolbar2.Hide()

    
    def OnStartCapture(self, event):
        self.toolbar1.EnableTool(1, False)
        self.toolbar1.EnableTool(2, True)
        self.notebook.SetSelection(3)
        self.sniffthread = SniffThread()


    def OnStopCapture(self, event):
        if self.sniffthread:
            self.toolbar1.EnableTool(1, True)
            self.toolbar1.EnableTool(2, False)
            print("Sniff Stopped")
            self.sniffthread.stop()


    def OnExit(self, event):
        self.Close(True)


    def OnAbout(self, event):
        panel = wx.Panel(self, wx.ID_ANY)
        info = wx.adv.AboutDialogInfo()
        info.SetName(NAME)
        info.SetVersion(VERSION)
        info.SetDescription(wordwrap(DESCRIPTION, 500, wx.ClientDC(panel)))
        info.SetCopyright(COPYRIGHT)
        info.SetWebSite(WEBSITE)
        info.SetLicense(wordwrap(LICENSE, 500, wx.ClientDC(panel)))
        wx.adv.AboutBox(info)


if __name__ == "__main__":
    app = wx.App()
    window = Seeker(None, title="Seeker", size=(1000, 600))
    window.Show()
    app.MainLoop()
