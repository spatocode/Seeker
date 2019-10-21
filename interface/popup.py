import wx

class PopupMenu(wx.Menu):
    def __init__(self, parent):
        super(PopupMenu, self).__init__()
        self.parent = parent

        sendPackets = wx.MenuItem(self, wx.NewId(), "Send Packets")
        self.Append(sendPackets)

        copyPackets = wx.MenuItem(self, wx.NewId(), "Copy Packets")
        self.Append(copyPackets)

        whois = wx.MenuItem(self, wx.NewId(), "Whois")
        self.Append(whois)

        filterPackets = wx.MenuItem(self, wx.NewId(), "Filter")
        self.Append(filterPackets)

        rts = wx.MenuItem(self, wx.NewId(), "Reconstruct TCP Session")
        self.Append(rts)

        rus = wx.MenuItem(self, wx.NewId(), "Reconstruct UDP Session")
        self.Append(rus)

        copyAddress = wx.MenuItem(self, wx.NewId(), "Copy Address")
        self.Append(copyAddress)
