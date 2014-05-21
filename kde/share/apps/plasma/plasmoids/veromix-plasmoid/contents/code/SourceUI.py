# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012 Nik Lutz <nik.lutz@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import *
from PyKDE4.plasma import Plasma

import signal, os, datetime
from LabelSlider import *
from Channel import *
from MuteButton  import *
from ClickableMeter import *

class SourceUI( Channel ):
    def __init__(self , parent):
        Channel.__init__(self, parent)

    def createMute(self):
        self.mute = InputMuteButton(self)
        self.mute.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum,True) )
        self.connect(self.mute, SIGNAL("clicked()"), self.on_mute_cb  )
        self.mute.setBigIconName("audio-input-microphone.png")

    def context_menu_create_custom(self):
        self.context_menu_create_ports()
        self.context_menu_create_sounddevices()

    def update_label(self):
        text =  ""
        bold = self.pa_sink.get_nice_title()
        if self.slider:
            self.slider.setText(text )
            self.slider.setBoldText(bold)
        self.set_name(bold)

    def on_update_meter(self, index, value, number_of_sinks):
        if self.index == index:
            self.slider.set_meter_value(int(value))

    def updateIcon(self):
        if self.isMuted():
            self.mute.setMuted(True)
        else:
            self.mute.setMuted(False)

## Drag and Drop Support

    def dropEvent(self, dropEvent):
        uris = dropEvent.mimeData().urls()
        for uri in uris:
            if uri.scheme() == "veromix":
                self.pa.move_source_output(uri.port(), self.index)
