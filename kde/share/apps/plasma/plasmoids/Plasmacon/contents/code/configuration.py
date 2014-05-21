# -*- coding: utf-8 -*-
#
#   Copyright (C) 2009 Andrey Shamakhov <shamakhov.a@gmail.com>
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

class MainOptions(QWidget):
    usetabs = False

    def __init__(self, usetabs):
        QWidget.__init__(self)

        self.usetabs = usetabs

        self.verticalLayout = QVBoxLayout(self)

        self.widget = QWidget(self)
        self.formLayout = QFormLayout(self.widget)
        self.chbUseTabs = QCheckBox(self.widget)
        if usetabs:
            self.chbUseTabs.setCheckState(Qt.Checked)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.chbUseTabs)
        self.verticalLayout.addWidget(self.widget)
        self.connect(self.chbUseTabs, SIGNAL("stateChanged(int)"), self.checkboxStateChanged)
        self.retranslateUi()

    @pyqtSignature("int")
    def checkboxStateChanged(self, i):
        self.usetabs = True if self.chbUseTabs.checkState() else False

    def retranslateUi(self):
        self.chbUseTabs.setText( ki18n("Use tabs (You should remove the applet and add it again)").toString() )

