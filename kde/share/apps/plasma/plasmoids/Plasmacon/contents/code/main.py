# -*- coding: utf-8 -*-
#
#   Copyright (C) 2012 Andrey Shamakhov <shamakhov.a@gmail.com>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License version 2,
#   or (at your option) any later version, as published by the Free
#   Software Foundation
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the
#   Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyKDE4.kio import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kparts import KParts

from configuration import MainOptions


class ConsoleWidget:
    part = None
    app = None
    layout = None
    border = None

class Plasmacon(plasmascript.Applet):

    def __init__(self, parent, args=None):
        super(Plasmacon, self).__init__(parent)
        self.setApplet(Plasma.Applet(parent, []))
        self.parent = parent
        #self.applet.setPopupIcon(KIcon("terminal"))
        #self.applet.togglePopup()

    def saveGeometry(self):
        fc = self.extConfig.group("settings")
        if ((self.applet.geometry().width() > 280) and (self.applet.geometry().height() > 55)):
            fc.writeEntry("width", QVariant(int(self.applet.geometry().width())))
            fc.writeEntry("height", QVariant(int(self.applet.geometry().height())))
    
    def init(self):        
        self.cwidgets = []
        self.existedSessions = []
        self.btnClosePressed = False
        self.signalDestroydOccured = False
        self.usetabs = True
        self.setHasConfigurationInterface(True)
        self.extConfig = KConfig( \
            KStandardDirs.locateLocal("config", "plasma_applet_plasmaconrc"))
        KMessageBox.setDontShowAskAgainConfig(self.extConfig)
        fc = self.extConfig.group("settings")
        if fc.readEntry("usetabs").compare("true"):
             self.usetabs = False
        fc = self.extConfig.group("settings")
        fc.writeEntry("usetabs", QVariant(self.usetabs))
        
        width = 600
        height = 300
        try:
            height = int(fc.readEntry("height"))
            width = int(fc.readEntry("width"))
        except ValueError, e:
            fc.writeEntry("width", QVariant(width))
            fc.writeEntry("height", QVariant(height))
            print str(e), ": Setting default geometry (600x300)."
        self.applet.resize(width, height)
        self.connect(self.applet, SIGNAL("geometryChanged()"), self.saveGeometry)

        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        self.setOpacity(.98)
        self.setPassivePopup(True)
        
        self.widget = QGraphicsWidget()
        self.applet.setPopupIcon(KIcon("utilities-terminal"))
        
        service = KService.serviceByDesktopName("konsolepart");
        self.factory = KPluginLoader(service.library()).factory()
                
        if self.factory:
            if self.usetabs:
                self.initWithTabs()
            else:
                self.initWithoutTabs()
            self.setGraphicsWidget(self.widget)
        else:
            print "Error: libkonsolepart.so doesn't exist."

    def createNewSession(self, id, part):
        self.cwidgets.append(ConsoleWidget())

        self.cwidgets[id].part = part
        self.cwidgets[id].part.openUrl(KUrl.fromPath(os.environ['HOME']))

        self.connect(self.cwidgets[id].part,
                     SIGNAL("destroyed()"),
                     self.setSignalCloseState)
        self.connect(self.cwidgets[id].part,
                     SIGNAL("destroyed()"),
                     self.closeTab)

        self.cwidgets[id].app = QGraphicsProxyWidget(self.tabBar)
        index = len(self.cwidgets)
        if index > 1:
            for index in range(1, max(self.existedSessions)+2):
                if index not in self.existedSessions:
                    break
        self.existedSessions.append(index)

        self.cwidgets[id].app.setWidget(self.cwidgets[id].part.widget())
        self.cwidgets[id].groupBox = Plasma.GroupBox()

        self.cwidgets[id].layout = \
            QGraphicsLinearLayout(Qt.Vertical,
                                  self.cwidgets[id].groupBox)
        self.cwidgets[id].layout.addItem(self.cwidgets[id].app)
        self.cwidgets[id].layout.setAlignment(self.cwidgets[id].app,
                                              Qt.AlignCenter)

        self.cwidgets[id].groupBox.setPreferredSize(3000, 3000)
        self.cwidgets[id].groupBox.setLayout(self.cwidgets[id].layout)

        self.tabBar.addTab(QString("Shell "+str(index)),
                           self.cwidgets[id].groupBox)
        self.tabBar.setCurrentIndex(id)
        self.setActiveSession(id)


    def addTab(self):
        currentTab = len(self.cwidgets)
        if currentTab < 51:
            part = self.factory.create()
            if part:
                self.createNewSession(currentTab, part)
            else:
                print "Error: can not create konsole part."
        else:
            print "You really need to have more than 50 opened sessions?!"

                
    def setBtnCloseState(self):
        self.btnClosePressed = True

    def setSignalCloseState(self):
        self.signalDestroydOccured = True

    def closeTab(self):
        id = self.tabBar.currentIndex()
        if (self.btnClosePressed and not self.signalDestroydOccured) or \
                (not self.btnClosePressed and self.signalDestroydOccured):
            self.existedSessions.remove(self.tabBar.tabText(id). \
                     split(QString(" ")).takeAt(1).toInt()[0])
            self.cwidgets.pop(id)
            self.tabBar.removeTab(id)

            # Trick that helps to repaint activeted tab's content
            # Still I've not found better decision :(
            id = self.tabBar.currentIndex()
            self.tabBar.addTab(QString(""))
            self.tabBar.setCurrentIndex(self.tabBar.count()-1)
            self.tabBar.setCurrentIndex(id)
            self.tabBar.removeTab(self.tabBar.count()-1)

            if self.tabBar.count() == 0:
                part = self.factory.create()
                if part:
                    self.createNewSession(0, part)
                else:
                    print "Error: can not create konsole part."

        if (self.btnClosePressed and self.signalDestroydOccured) or \
                (not self.btnClosePressed and self.signalDestroydOccured):
            self.signalDestroydOccured = False
            self.btnClosePressed = False
    
    def setActiveSession(self, index):
        if index < len(self.cwidgets):
            self.cwidgets[index].part.widget().repaint(0,0,1000,1000)
            self.cwidgets[index].part.widget().setFocus()


    def initWithTabs(self):
        self.widget.setMinimumSize(300, 155)
        self.hlayout = QGraphicsLinearLayout(Qt.Vertical, self.widget)
        self.vlayout = QGraphicsLinearLayout(Qt.Horizontal, self.hlayout)
        self.tabBar = Plasma.TabBar(self.widget)
        self.connect(self.tabBar,
                     SIGNAL("currentChanged(int)"),
                     self.setActiveSession)
        self.addTabBtn = Plasma.PushButton(self.widget)
        self.addTabBtn.setText(QString("New session"))
        self.addTabBtn.setMaximumHeight(25)
        self.addTabBtn.setMaximumWidth(125)

        self.closeTabBtn = Plasma.PushButton(self.widget)
        self.closeTabBtn.setText(QString("Close session"))
        self.closeTabBtn.setMaximumHeight(25)        
        self.closeTabBtn.setMaximumWidth(125)
        
        self.connect(self.addTabBtn,
                     SIGNAL("clicked()"),
                     self.addTab)
        self.connect(self.closeTabBtn,
                     SIGNAL("clicked()"),
                     self.setBtnCloseState)
        self.connect(self.closeTabBtn,
                     SIGNAL("clicked()"),
                     self.closeTab)

        spacer = Plasma.Label(self.widget)

        self.vlayout.addItem(self.addTabBtn)
        self.vlayout.addItem(spacer)
        self.vlayout.addItem(self.closeTabBtn)

        self.hlayout.addItem(self.tabBar)
        self.hlayout.addItem(self.vlayout)

        self.hlayout.setAlignment(self.tabBar, Qt.AlignCenter)

        self.vlayout.setAlignment(self.addTabBtn, Qt.AlignLeft)
        self.vlayout.setAlignment(spacer, Qt.AlignJustify | Qt.AlignBottom)
        self.vlayout.setAlignment(self.closeTabBtn, Qt.AlignRight)

        self.widget.setLayout(self.hlayout)
        
        part = self.factory.create()
        if part:
            self.createNewSession(0, part)
        else:
            print "Error: can not create konsole part."

    def startSingleSession(self):
        self.mainPart = self.factory.create()
        if self.mainPart:
            self.centralWidget = QGraphicsProxyWidget(self.groupBox)
            self.layout.addItem(self.centralWidget)
            self.layout.setAlignment(self.centralWidget, Qt.AlignCenter)
            self.mainPart.openUrl(KUrl.fromPath(os.environ['HOME']))
            self.consoleWidget = self.mainPart.widget()
            #self.shc = QShortcut(QKeySequence.Paste, self.consoleWidget)
            #self.shc = QShortcut(QKeySequence(Qt.Key_Control, Qt.Key_Shift, Qt.Key_V), self.consoleWidget)
            # QShortcut(Qt.SHIFT + Qt.CTRL + Qt.Key_V, self.consoleWidget)

            self.centralWidget.setWidget(self.consoleWidget)
            self.consoleWidget.setFocus()
            self.connect(self.mainPart,
                         SIGNAL("destroyed()"),
                         self.startSingleSession)
        else:
            print "Error: can not create konsole part."

    def initWithoutTabs(self):
        self.widget.setMinimumSize(280, 55)
        self.groupBox = Plasma.GroupBox(self.widget)

        self.appletLayout = QGraphicsLinearLayout(Qt.Vertical, self.widget)        
        self.appletLayout.addItem(self.groupBox)
        self.appletLayout.setAlignment(self.groupBox, Qt.AlignCenter)
   
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.groupBox)

        self.groupBox.setLayout(self.layout)
        self.widget.setLayout(self.appletLayout)
        self.startSingleSession()

    def configAccepted(self):
        if self.usetabs != self.mainOptions.usetabs:
            self.usetabs = self.mainOptions.usetabs
            fc = self.extConfig.group("settings")
            fc.writeEntry("usetabs", QVariant(self.usetabs))
        self.configDenied()
            
    def configDenied(self):
        self.mainOptions.deleteLater()

    def createConfigurationInterface(self, parent):
        self.mainOptions = MainOptions(self.usetabs)
        p = parent.addPage(self.mainOptions, ki18n("Misc Options").toString())
        p.setIcon( KIcon("utilities-terminal") )
        self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
        self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)

    def showConfigurationInterface(self):
        dialog = KPageDialog()
        dialog.setFaceType(KPageDialog.List)
        dialog.setButtons(KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel))
        self.createConfigurationInterface(dialog)
        dialog.resize(300,200)
        dialog.exec_()

def CreateApplet(parent):
    return Plasmacon(parent)

