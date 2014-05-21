from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import subprocess
import threading
import dbus
import time
import PyKDE4.kdecore

class MainApplet(plasmascript.Applet):
	def __init__(self,parent,args=None):
		plasmascript.Applet.__init__(self,parent)
		
	def init(self):
		layout=QGraphicsLinearLayout(Qt.Vertical, self.applet)
		self.label = Plasma.Label(self.applet)
		
		self.iconAddress = unicode(PyKDE4.kdecore.KGlobal.dirs().localkdedir()) + "share/apps/plasma/plasmoids/Bumblebee_Status/contents/"
		
		self.label.setImage(self.iconAddress + "inactive.png")
		layout.addItem(self.label)
		self.applet.setLayout(layout)
		self.displayIcon()
		self.status = "off"
		self.timer = QTimer()
		self.connect(self.timer,SIGNAL("timeout()"),self.displayIcon)
		self.timer.start(2000)
		
	def checkStatus(self):
		proc=subprocess.Popen('optirun --status | grep -c off', shell=True, stdout=subprocess.PIPE, )
		output=proc.communicate()[0]
		if output[0:1] == "1":
			if self.status == "on":
				self.statusChange(1)
			self.status = "off"
		else:
			if self.status == "off":
				self.statusChange(0)
			self.status = "on"
		return self.status
	
	def displayIcon(self):
		x = self.checkStatus()
		if x == "off":
			self.label.setImage(self.iconAddress + "inactive.png")
		else:
			self.label.setImage(self.iconAddress + "active.png")
		self.label.setScaledContents(True)
	
	def statusChange(self,x):
		knotify = dbus.SessionBus().get_object("org.kde.knotify", "/Notify")
		eventTime = time.strftime("%T")  
		#if x == 0:
			#knotify.event("warning", "kde", [], "Optimus Change - Activated", u"Discrete card switched ON @ %s"%(eventTime), [], [], 0, 0, dbus_interface="org.kde.KNotify")
		#else:
			#knotify.event("warning", "kde", [], "Optimus Change - Deactivated", u"Discrete Card switched OFF @ %s"%(eventTime), [], [], 0, 0, dbus_interface="org.kde.KNotify")
 
def CreateApplet(parent):
	return MainApplet(parent)