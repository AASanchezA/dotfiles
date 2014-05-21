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
from SinkUI import *
from Channel import *
from MuteButton  import InputMuteButton

class InputSinkUI(SinkUI):

    def __init__(self, parent):
        self.mouse_pressed = False
        SinkUI.__init__(self, parent)
        self.setAcceptDrops(False)
        self.setContentsMargins(0,0,0,0)
        self.layout.setContentsMargins(6,2,6,0)

    def createMute(self):
        self.mute = InputMuteButton(self)
        self.mute.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed,True))
        self.connect(self.mute, SIGNAL("clicked()"), self.on_mute_cb)

    def context_menu_create_custom(self):
        self.create_menu_switch_sink()
        self.create_menu_ladspa_effects()

    def create_menu_kill_sink(self):
        self.action_kill = QAction(i18n("Disconnect/kill"), self.popup_menu)
        self.popup_menu.addAction(self.action_kill)
        self.action_kill.triggered.connect(self.on_contextmenu_clicked)

    def context_menu_create_settings(self):
        pass

    def create_menu_switch_sink(self):
        sink_menu = QMenu(i18n("Move To"), self.popup_menu)
        sinks = self.veromix.get_sink_widgets()
        for sink in sinks:
            action = QAction(sink.name(), self.popup_menu)
            sink_menu.addAction(action)
        self.popup_menu.addMenu(sink_menu)

    def create_menu_ladspa_effects(self):
        if not self.veromix.is_ladspa_enabled():
            return

    def context_menu_create_effects(self):
        pass

    def on_contextmenu_clicked(self, action):
        if type(action) == bool:
            return
        if action.text() == self.action_kill.text():
            self.sink_input_kill()
            return 0
        # search ouputs for text, and move sink_input
        for sink in self.veromix.get_sink_widgets():
            if action.text() == sink.name():
                self.pa.move_sink_input(self.index, int(sink.index))
                return 0

    def getOutputIndex(self):
        return self.pa_sink.props["sink"]

    def update_label(self):
        text =  self.pa_sink.name
        bold = self.pa_sink.props["app"]

        iconname = None
        if self.pa_sink.props["app_icon"] != "None":
            iconname = self.pa_sink.props["app_icon"]
        if iconname == None and  self.pa_sink.props["app"] != "None":
            iconname = self.veromix.query_application(self.pa_sink.props["app"])
        if bold == "knotify":
            bold = i18n("Event Sounds")
            text = ""
            iconname = 'dialog-information'
        if bold == "npviewer.bin" or bold == "plugin-container":
            bold = i18n("Flash Player")
            text = ""
            iconname = 'flash'
        if bold == "chromium-browser":
            bold = i18n("Chromium Browser")
            text = ""
        if bold == "Skype":
            if text == "Event Sound":
                text = i18n("Event Sound")
            if text == "Output":
                text = i18n("Voice Output")

        if text == "LADSPA Stream" or (self.pa_sink.props["media.name"] == "LADSPA Stream"):
            for sink in self.veromix.get_sink_widgets():
                if sink.pa_sink.props["owner_module"] == self.pa_sink.props["owner_module"]:
                    bold = sink.pa_sink.props["device.ladspa.name"]
                    text = ""
                    iconname = sink.pa_sink.props["device.icon_name"]

        # FIXME
        if bold in ["", "None", None]:
            bold = text
            text = ""

        if text in ["None", None]:
            text = ""

        if iconname in ["", "None", None]:
            iconname = "mixer-pcm"

        if iconname :
            self.mute.setBigIconName(iconname)
            self.updateIcon()

        if self.slider:
            self.set_name(bold)
            self.slider.setText(text)
            self.slider.setBoldText(bold)

### Drag and Drop

    def mousePressEvent(self, event):
        self.mouse_pressed = True

    def mouseReleaseEvent(self, event):
        self.mouse_pressed = False

    def mouseMoveEvent(self,e):
        if self.mouse_pressed :
            self.startDrag(e)

    def startDrag(self,event):
        drag = QDrag(event.widget())
        drag.setPixmap(self.mute.icon().pixmap(self.size().height(),self.size().height()))
        mimedata = QMimeData()
        liste = []
        liste.append(QUrl( "veromix://sink_input_index:" + str(int(self.index))))
        mimedata.setUrls(liste)
        drag.setMimeData(mimedata)
        #drag.setHotSpot(event.pos() - self.rect().topLeft())
        dropAction = drag.start(Qt.MoveAction)

