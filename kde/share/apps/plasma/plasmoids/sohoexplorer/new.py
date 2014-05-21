from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kdeui import * 
from PyKDE4.kdecore import * 
from StringIO import StringIO
import os, urllib2, socket, sys
import Image

socket.setdefaulttimeout(10)

def toint(i):
    if isinstance(i, QVariant) or isinstance(i, QString):
        return int(i.toInt()[0])
    else:
        return int(i)

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
        cg = self.config()
        self.updateinterval = toint(cg.readEntry("interval","300000")
        self.url = self.urls[toint(cg.readEntry("url","2"))]
        self.prevsize = toint(cg.readEntry("size","542"))
        self.resize(self.prevsize, self.prevsize)
        self.outfile = os.path.join(str(self.applet.package().path()),"sol.jpg")
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
            self.config().writeEntry("size",int(self.size().height()))
            self.setBackgroundHints(Plasma.Applet.DefaultBackground)
            self.inPanel = False
            self.update()

    def paintInterface(self, painter, option, rect):
        if os.path.getsize(self.outfile) == 0L:
            painter.drawText(rect, Qt.AlignVCenter | Qt.AlignHCenter, ki18n( "Error fetching image" ).toString() )
            return
        image = QPixmap(self.outfile)
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
        out = file(self.outfile, "w")
        try:
            chart = urllib2.urlopen(url).read()
        except urllib2.URLError, e:
            sys.stderr.write("Failed to get chart. %s" % e)
            return False
        out.write(chart)
        out.close()
        return True

    def createConfigurationInterface(self, parent):
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
        self.kcombobox.setCurrentIndex(int(self.readConfig("url","2")))
        self.kcombobox.setObjectName("viewchooser")
        #self.label = QLabel(dialog)
        #self.label.setGeometry(QRect(10, 0, 101, 17))
        #self.label.setObjectName("label")
        #self.label.setText( ki18n( "Solar View" ).toString() )
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
        cg = self.config()
        self.url = self.urls[self.kcombobox.currentIndex()]
        cg.writeEntry("url",self.kcombobox.currentIndex())
        self.getimage(self.url)
        self.update()

    def readConfig(self, option, default):
        if os.path.isfile(self.config):    
            settings = file(self.config, 'r').readlines()
            for i in settings:
                if i.startswith(option):
                    return i.split("=")[1]
        else:   
            return default
        return default

    def writeConfig(self, option, value):
        if os.path.isfile(self.config):
            settings = file(self.config, 'r')
            lines = settings.readlines()
            for i in range(len(lines)):
                if lines[i].startswith(option):
                    lines[i] = "%s=%s" % (option, value)
                    settings = file(self.config, 'w')
                    settings.write('\n'.join(lines))
                    settings.close()
                    return
            settings = file(self.config, 'w')
            lines.append("%s=%s" % (option, value))
            settings.write('\n'.join(lines))
            settings.close()
        else:
            settings = file(self.config, 'w')
            lines = ["%s=%s\n" % (option, value)]
            settings.writelines(lines)
            settings.close()

def CreateApplet(parent):
    return Solar(parent)
