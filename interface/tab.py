import wx
import wx.dataview
import time
from wx.lib.pubsub import pub
from interface.popup import PopupMenu

class ScanResults(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.listctrl = wx.dataview.DataViewListCtrl(self, wx.ID_ANY)
        self.listctrl.AppendTextColumn("Status")
        self.listctrl.AppendTextColumn("Name")
        self.listctrl.AppendTextColumn("IP")
        self.listctrl.AppendTextColumn("MAC address")
        self.listctrl.AppendTextColumn("Manufacturer")

        pub.subscribe(self.updateDisplay, "updateScanResult")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.listctrl, 1, wx.EXPAND, 5)
        self.SetSizer(sizer)

    def updateDisplay(self, msg):
        if isinstance(msg, list):
            if self.listctrl.GetItemCount() > 0:
                if msg[2] == self.listctrl.GetTextValue(0,2):
                    self.listctrl.DeleteAllItems()
            self.listctrl.AppendItem(msg)


class SavedComputers(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # Todo: Use IsRowSelected() to trigger row popupmenu
        self.listctrl = wx.dataview.DataViewListCtrl(self, wx.ID_ANY)
        self.listctrl.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self.listctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnRightDown)

        self.status = self.listctrl.AppendTextColumn("Status")
        self.name = self.listctrl.AppendTextColumn("Name")
        self.ip = self.listctrl.AppendTextColumn("IP")
        self.mac = self.listctrl.AppendTextColumn("MAC address")
        self.man = self.listctrl.AppendTextColumn("Manufacturer")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.listctrl, 1, wx.EXPAND, 5)
        self.SetSizer(sizer)

    def updateDisplay(self, msg):
        if isinstance(msg, list):
            if self.listctrl.GetItemCount() > 0:
                if msg[2] == self.listctrl.GetTextValue(0,2):
                    error = "A computer with this IP address already exists"
                    dialog = wx.MessageDialog(None, error, "Error", wx.OK | wx.ICON_EXCLAMATION)
                    dialog.ShowModal()
                    return
            self.listctrl.AppendItem(msg)

    def OnRightDown(self, event):
        print("POS", event.GetPosition())
        #self.PopupMenu(PopupMenu(self), event.GetPosition())

    def OnContextMenu(self, event):
        popupmenu = wx.Menu()
        self.statusItem = popupmenu.Append(wx.ID_ANY, "Status", "Status", kind=wx.ITEM_CHECK)
        self.nameItem = popupmenu.Append(wx.ID_ANY, "Name", "Name", kind=wx.ITEM_CHECK)
        self.ipItem = popupmenu.Append(wx.ID_ANY, "IP", "IP", kind=wx.ITEM_CHECK)
        self.macItem = popupmenu.Append(wx.ID_ANY, "MAC address", "MAC address", kind=wx.ITEM_CHECK)
        self.manItem = popupmenu.Append(wx.ID_ANY, "Manufacturer", "Manufacturer", kind=wx.ITEM_CHECK)

        popupmenu.Check(self.statusItem.GetId(), True)
        popupmenu.Check(self.nameItem.GetId(), True)
        popupmenu.Check(self.ipItem.GetId(), True)
        popupmenu.Check(self.macItem.GetId(), True)
        popupmenu.Check(self.manItem.GetId(), True)

        self.Bind(wx.EVT_MENU, self.OnToggleStatus, self.statusItem)
        self.Bind(wx.EVT_MENU, self.OnToggleName, self.nameItem)
        self.Bind(wx.EVT_MENU, self.OnToggleIP, self.ipItem)
        self.Bind(wx.EVT_MENU, self.OnToggleMac, self.macItem)
        self.Bind(wx.EVT_MENU, self.OnToggleMan, self.manItem)

        self.PopupMenu(popupmenu, event.GetPosition())
    
    def OnToggleStatus(self, event):
        if self.statusItem.IsChecked():
            print("insert")
            self.listctrl.InsertColumn(0, self.status)
        else:
            print("delete")
            self.listctrl.DeleteColumn(self.status)

    def OnToggleName(self, event):
        if self.nameItem.IsChecked():
            self.name.Show()
        else:
            self.name.Hide()

    def OnToggleIP(self, event):
        if self.ipItem.IsChecked():
            self.ip.Show()
        else:
            self.ip.Hide()

    def OnToggleMac(self, event):
        if self.macItem.IsChecked():
            self.mac.Show()
        else:
            self.mac.Hide()

    def OnToggleMan(self, event):
        if self.manItem.IsChecked():
            self.man.Show()
        else:
            self.man.Hide()
    

class IPConnections(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.listctrl = wx.dataview.DataViewListCtrl(self, wx.ID_ANY)
        self.listctrl.AppendTextColumn("Time")
        self.listctrl.AppendTextColumn("Local IP")
        self.listctrl.AppendTextColumn("Remote IP")
        self.listctrl.AppendTextColumn("Received")
        self.listctrl.AppendTextColumn("Sent")
        self.listctrl.AppendTextColumn("Direction")
        self.listctrl.AppendTextColumn("Port")
        self.listctrl.AppendTextColumn("Hostname")
        self.listctrl.AppendTextColumn("Size")
        self.listctrl.AppendTextColumn("Process")

        pub.subscribe(self.updateDisplay, "updateIPConn")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.listctrl, 1, wx.EXPAND, 5)
        self.SetSizer(sizer)

    def updateDisplay(self, msg):
        if isinstance(msg, list):
            self.listctrl.AppendItem(msg)


class Whois(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is whois utility", (20,20))


class Packets(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.listctrl = wx.dataview.DataViewListCtrl(self, wx.ID_ANY)
        self.listctrl.AppendTextColumn("No")
        self.listctrl.AppendTextColumn("Protocol")
        self.listctrl.AppendTextColumn("Src MAC")
        self.listctrl.AppendTextColumn("Dest MAC")
        self.listctrl.AppendTextColumn("Src IP")
        self.listctrl.AppendTextColumn("Dest IP")
        self.listctrl.AppendTextColumn("Src Port")
        self.listctrl.AppendTextColumn("Dest Port")
        self.listctrl.AppendTextColumn("Time")
        self.listctrl.AppendTextColumn("Size")

        pub.subscribe(self.updateDisplay, "updatePackets")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.listctrl, 1, wx.EXPAND, 5)
        self.SetSizer(sizer)

    def updateDisplay(self, msg):
        if isinstance(msg, list):
            self.listctrl.AppendItem(msg)

class VoIP(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is VoIP", (20,20))

class NoteBook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        self.scanResults = ScanResults(self)
        self.savedComputers = SavedComputers(self)
        self.whois = Whois(self)
        self.ipConnection = IPConnections(self)
        self.packets = Packets(self)
        self.voip = VoIP(self)

        self.AddPage(self.scanResults, "Scan Results")
        self.AddPage(self.savedComputers, "Saved Computers")
        self.AddPage(self.whois, "Whois")
        self.AddPage(self.ipConnection, "Latest IP Connections")
        self.AddPage(self.packets, "Packets")
        self.AddPage(self.voip, "VoIP")

        # il = wx.ImageList(16, 16)
        # idxl = il.Add(wx.Bitmap("assets/newfile.png"))
        # self.AssignImageList(il)
        # self.SetPageImage(0, idxl)
