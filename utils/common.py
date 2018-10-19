import wx
import textwrap

def scale_image(path):
    image = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
    img = image.ConvertToImage()
    image = wx.Bitmap(img.Scale(30, 30))
    return image
