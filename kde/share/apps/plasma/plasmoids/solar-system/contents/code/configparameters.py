from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import *
from PyKDE4.kio import *
from PyKDE4.kdecore import *
from ui_configparameters import Ui_Form

class ConfigParameters(QWidget, Ui_Form):
  def __init__(self, parent, settings):
    QWidget.__init__(self)

    self.setupUi(self)
    self.parent = parent

    if settings["showOrbits"] == "true":
       self.showOrbits.setChecked(True)
    else:
       self.showOrbits.setChecked(False)

    if settings["showLegend"] == "true":
       self.showLegend.setChecked(True)
    else:
       self.showLegend.setChecked(False)

    if settings["showPluto"] == "true":
       self.showPluto.setChecked(True)
    else:
       self.showPluto.setChecked(False)

    self.textcolor.setColor(QColor(settings["textcolor"]))
    self.orbitcolor.setColor(QColor(settings["orbitcolor"]))
    #self.mysize = settings["mysize"]
 

  # update a given settings-instance
  def updateSettings(self, settings):
    if self.showOrbits.isChecked():
       settings["showOrbits"] = "true"
    else:
       settings["showOrbits"] = "false"


    if self.showLegend.isChecked():
       settings["showLegend"] = "true"
    else:
       settings["showLegend"] = "false"

    if self.showPluto.isChecked():
       settings["showPluto"] = "true"
    else:
       settings["showPluto"] = "false"

    qcol = self.textcolor.color().name()
    settings["textcolor"] = str(qcol)
    qcol = self.orbitcolor.color().name()
    settings["orbitcolor"] = str(qcol)
    #settings["mysize"] = self.mysize
 