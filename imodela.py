#!/usr/bin/env python
#-*- coding:utf-8 -*-

import wx
import os
import commands

class MyFrame(wx.Frame):
    def __init__(self,parent,id,title):
        self.filename = None
        wx.Frame.__init__(self,parent,id,title,wx.DefaultPosition,wx.DefaultSize)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox3 = wx.BoxSizer(wx.VERTICAL)

        hbox1.Add(wx.StaticText(self,-1,"Connect to:"),1,wx.ALL,5)
        printer_names = self.getPrinters()
        self.combo = wx.ComboBox(self, 4,choices=printer_names, style=wx.CB_READONLY)
        hbox1.Add(self.combo,1,wx.ALL,5)
        hbox1.Add(wx.Button(self,3,"info"),1,wx.ALL,5)

        hbox2.Add(wx.StaticText(self,-1,"GCode:"),1,wx.ALL,5)
        self.textCtrl = wx.TextCtrl(self,-1)
        hbox2.Add(self.textCtrl,1,wx.ALL,5 )
        hbox2.Add(wx.Button(self,4,"Send"),1,wx.ALL,5)

        vbox1.Add(wx.StaticText(self,-1,"Choose file:"),1,wx.ALL,5)
        vbox1.Add(wx.Button(self,1,"select file"),1,wx.ALL,5)
        self.selectedFile = wx.StaticText(self,-1,"file not selected")
        vbox2.Add(self.selectedFile,1,wx.EXPAND,5)
        vbox2.Add(wx.Button(self,2,"send file"),1,wx.ALL|wx.ALIGN_RIGHT,5)
        hbox3.Add(vbox1,1,wx.ALL)
        hbox3.Add(vbox2,1,wx.EXPAND)

        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc.InsertColumn(0, 'Queue ID')
        self.lc.SetColumnWidth(0, 250)
        vbox3.Add(wx.Button(self,5,"refresh job queue"),1,wx.ALL,5)
        vbox3.Add(wx.Button(self,6,"cancel all jobs"),1,wx.ALL,5)
        hbox4.Add(self.lc,1,wx.ALL|wx.EXPAND)
        hbox4.Add(vbox3,1,wx.ALL)

        vbox.Add(hbox1,1,wx.ALL)        
        vbox.Add(hbox2,1,wx.ALL)
        vbox.Add(hbox3,1,wx.ALL)
        vbox.Add(hbox4,1,wx.ALL)
        self.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON,self.loadFile,id=1)
        self.Bind(wx.EVT_BUTTON,self.sendRml,id=2)
        self.Bind(wx.EVT_BUTTON,self.showPrinter,id=3)
        self.Bind(wx.EVT_BUTTON,self.sendGcode,id=4)
        self.Bind(wx.EVT_BUTTON,self.getQueues,id=5)
        self.Bind(wx.EVT_BUTTON,self.cancelQueues,id=6)

    def sendGcode(self,event):
        printer_name = self.combo.GetValue()
        command = "lpr -P "+ printer_name +" "+ self.textCtrl.GetValue()
        print command

    def showPrinter(self,event):
        printer_name = self.combo.GetValue()
        wx.MessageBox(printer_name + " is selected.",'Info', wx.OK | wx.ICON_ERROR)

    def loadFile(self, event):
        self.filename = wx.FileSelector(default_path=os.getcwd())
        if not (self.filename == ""):
            self.selectedFile.SetLabel(self.filename)
            (frameX,frameY) = self.Size
            self.SetSize((frameX+1,frameY+1))

    def sendRml(self,event):
        printer_name = self.combo.GetValue()
        if(self.filename == None):
            wx.MessageBox("No RML file selected.",'Error', wx.OK | wx.ICON_ERROR)
        else:
            dlg = wx.MessageDialog(self,"Sending file "+self.filename, "Are you sure?", wx.YES_NO | wx.ICON_QUESTION) 
            result = dlg.ShowModal() == wx.ID_YES
            dlg.Destroy()
            if(result):
                print "send data..."
                file = open(self.filename).read()
                print file
                command = "lpr -P "+printer_name+" "+self.filename
                os.system(command)

    def getQueues(self,event):
        status, output = commands.getstatusoutput("lpstat")
        queueIDs = [queue.split()[0] for queue in output.split("\n")]
        self.lc.DeleteAllItems()
        for queueID in queueIDs:
            self.lc.InsertStringItem(queueIDs.index(queueID),queueID)

    def cancelQueues(self,event):
        return 

    def getPrinters(self):
        status, output = commands.getstatusoutput("lpstat -s")
        printers = output.split("\n")
        printer_names = [printer.split("device for")[1].split(":")[0].strip() for printer in printers if "device for" in printer]
        return printer_names


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None,-1,'iModela communicator')
        frame.Show()
        return True

app = MyApp(0)
app.MainLoop()
