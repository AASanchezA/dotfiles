#   -*- coding: utf-8 -*-                                       
#                                                               
#   Copyright (C) 2009 eightmillion <eightmillion@gmail.com>              
#                                                               
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License as     
#   published by the Free Software Foundation; either version 2, or     
#   (at your option) any later version.                                 
#                                                                       
#   This program is distributed in the hope that it will be useful,     
#   but WITHOUT ANY WARRANTY; without even the implied warranty of      
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the       
#   GNU General Public License for more details                         
#                                                                       
#   You should have received a copy of the GNU Library General Public   
#   License along with this program; if not, write to the               
#   Free Software Foundation, Inc.,                                     
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.       
#   
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kdeui import * 
from PyKDE4.kdecore import * 
import os, urllib2, socket, sys

socket.setdefaulttimeout(10)

class Solar(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

    def init(self):
        self.urls = [
                "http://sohowww.nascom.nasa.gov/data/realtime/eit_171/512/latest.jpg",
                "http://sohowww.nascom.nasa.gov/data/realtime/eit_195/512/latest.jpg",
                "http://sohowww.nascom.nasa.gov/data/realtime/eit_284/512/latest.jpg",
                "http://sohowww.nascom.nasa.gov/data/realtime/eit_304/512/latest.jpg",
                "http://sohowww.nascom.nasa.gov/data/realtime/mdi_igr/512/latest.jpg",
                "http://sohowww.nascom.nasa.gov/data/realtime/mdi_mag/512/latest.jpg",
                "http://sohowww.nascom.nasa.gov/data/realtime/c2/512/latest.jpg",
                "http://sohowww.nascom.nasa.gov/data/realtime/c3/512/latest.jpg",
        ]
        gc = self.config()
        self.updateinterval = gc.readEntry("interval", QVariant(300000) ).toInt()[0]
        self.url = self.urls[gc.readEntry("url", QVariant(3) ).toInt()[0]]
        self.prevsize = gc.readEntry("size", QVariant(542) ).toInt()[0]
        self.resize(self.prevsize, self.prevsize)
        self.image = QImage.fromData("")
        self.inPanel = False
        self.setAspectRatioMode(Plasma.Square)
        self.startTimer(self.updateinterval)
        self.height = self.size().height() - 30
        self.width = self.size().width() - 30
        self.getimage(self.url)
 
    def constraintsEvent(self, constraints):
        if self.formFactor() == Plasma.Horizontal or self.formFactor() == Plasma.Vertical:
            # In the panel.
            self.setBackgroundHints(Plasma.Applet.NoBackground)
            self.inPanel = True
            self.getimage(self.url)
            self.height = self.size().height() 
            self.width = self.size().width() 
            self.update()
        else:
            self.height = self.size().height() - 30
            self.width = self.size().width() - 30
            gc = self.config()
            gc.writeEntry("size", QVariant(int(self.size().height())) )
            self.setBackgroundHints(Plasma.Applet.DefaultBackground)
            self.inPanel = False
            self.update()

    def paintInterface(self, painter, option, rect):
        if self.image.size().width() == 0:
            painter.drawText(rect, Qt.AlignVCenter | Qt.AlignHCenter, ki18n( "Error fetching image" ).toString() )
            return
        image = QPixmap.fromImage(self.image)
        image = image.scaled(self.width, self.height)
        if self.inPanel:
            painter.drawPixmap(0, 0, image)
        else:
            painter.drawPixmap(15, 15, image)
        #painter.save()
        #painter.setPen(Qt.white)
        #painter.setFont(QFont('Segoe Semibold', 6))
        #painter.drawText(10, 5, "111112222")
        #painter.drawText(10,15, "123456789012234567890")
        #painter.restore()

    def timerEvent(self, event):
        self.getimage(self.url)    
        sys.stderr.write("Updating...\n")
        self.update()

    def getimage(self, url):
        try:
            chart = urllib2.urlopen(url).read()
        except urllib2.URLError, e:
            sys.stderr.write("Failed to get chart. %s" % e)
            self.image = QImage.fromData("")
            return False
        self.image = QImage.fromData(chart)
        return True

    def createConfigurationInterface(self, parent):
        gc = self.config()
        parent.setWindowTitle( ki18n( "Solar Observatory Settings" ).toString() )
        self.miscSettings = QWidget(parent)
        self.miscSettings.setObjectName("General Settings")
        self.kcombobox = KComboBox(self.miscSettings)
        self.kcombobox.setIconSize(QSize(64,64))
        self.kcombobox.insertItem(0,QIcon( os.path.join( str(self.applet.package().path()), "icons/eit171.jpg")),
                                  "EIT 171\nExtreme ultraviolet Imaging Telescope\n171 Angstrom, 1 million Kelvin")
        self.kcombobox.insertItem(1,QIcon( os.path.join( str(self.applet.package().path()), "icons/eit195.jpg")),
                                  "EIT 195\nExtreme ultraviolet Imaging Telescope\n195 Angstrom, 1.5 million Kelvin")
        self.kcombobox.insertItem(2,QIcon( os.path.join( str(self.applet.package().path()), "icons/eit284.jpg")),
                                  "EIT 284\nExtreme ultraviolet Imaging Telescope\n284 Angstrom, 2 million Kelvin")
        self.kcombobox.insertItem(3,QIcon( os.path.join( str(self.applet.package().path()), "icons/eit304.jpg")),
                                  "EIT 304\nExtreme ultraviolet Imaging Telescope\n304 Angstrom, 60,000 to 80,000 Kelvin")
        self.kcombobox.insertItem(4,QIcon( os.path.join( str(self.applet.package().path()), "icons/mdicontinuum.jpg")),
                                  "MDI Continuum\nMichelson Doppler Imager\nNear the Ni I 6768 Angstrom line")
        self.kcombobox.insertItem(5,QIcon( os.path.join( str(self.applet.package().path()), "icons/mdimagnetogram.jpg")),
                                  "MDI Magnetogram\nMichelson Doppler Imager\nNear the Ni I 6768 Angstrom line")
        self.kcombobox.insertItem(6,QIcon( os.path.join( str(self.applet.package().path()), "icons/lascoc2.jpg")),
                                  "Lasco C2\nLarge Angle Spectrometric Coronagraph\nInner solar corona up to 8.4 million kilometers away")
        self.kcombobox.insertItem(7,QIcon( os.path.join( str(self.applet.package().path()), "icons/lascoc3.jpg")),
                                  "Lasco C2\nLarge Angle Spectrometric Coronagraph\nOuter solar corona up to 45 million kilometers away")
        self.kcombobox.setGeometry(QRect(10, 0, 340, 74))
        self.kcombobox.setCurrentIndex(gc.readEntry("url", QVariant(2) ).toInt()[0])
        self.kcombobox.setObjectName("viewchooser")
        self.settingspage = KPageWidgetItem(self.miscSettings, ki18n( "General Settings" ).toString() )
        self.settingspage.setHeader( ki18n( "Solar View" ).toString() )
        self.settingspage.setIcon( KIcon( "preferences-desktop-color" ) )

        parent.addPage(self.settingspage)

    def showConfigurationInterface(self):
        dialog = KPageDialog(None)
        self.createConfigurationInterface(dialog)
        dialog.setButtons( KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel) )
        dialog.resize( 380, 160 )
        self.connect(dialog, SIGNAL("okClicked()"), self, SLOT("configAccepted()"))
        dialog.exec_()

    @pyqtSignature("configAccepted()")
    def configAccepted(self):
        self.url = self.urls[self.kcombobox.currentIndex()]
        gc = self.config()
        gc.writeEntry("url", QVariant(self.kcombobox.currentIndex()) )
        self.getimage(self.url)
        self.update()

def CreateApplet(parent):
    return Solar(parent)
