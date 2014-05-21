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

import datetime

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import *
from PyKDE4.plasma import Plasma
from PyKDE4.kdecore import i18n

from Channel import Channel

class SinkUI(Channel):
    muteInfo = pyqtSignal(bool)

    def __init__(self , parent):
        self.automatically_muted = False
        self.extended_panel = None
        Channel.__init__(self, parent)
        self.setContentsMargins(0,0,0,0)

    def context_menu_create_custom(self):
        self.context_menu_create_ports()
        self.context_menu_create_sounddevices()
        action_device = QAction(i18n("Default Sink"), self.popup_menu)
        self.popup_menu.addAction(action_device)
        action_device.setCheckable(True)
        if self.isDefaultSink():
            action_device.setChecked(True)
            action_device.setEnabled(False)
        else:
            action_device.setChecked(False)
            action_device.setEnabled(True)
            action_device.triggered.connect(self.on_set_default_sink_triggered)

    def create_menu_kill_sink(self):
        Channel.create_menu_kill_sink(self)
        if self.pa_sink.props["driver"]=="module-combine-sink.c":
            action=QAction(i18n("Uncombine"), self.popup_menu)
            self.popup_menu.addAction(action)
            action.triggered.connect(self.stopcombining)
        self.context_menu_create_sounddevices_other()

    def context_menu_create_effects(self):
        if not self.veromix.is_ladspa_enabled():
            return
        effects_menu = QMenu(i18n("Add Effect"), self.popup_menu)
        effects_menu.triggered.connect(self.on_add_ladspa_effect)
        self.popup_menu.addMenu(effects_menu)

        self.populate_presets_menu(effects_menu, None, False)
        self.populate_switch_effect_menu(effects_menu, None)

    def stopcombining(self, action):
        self.pa_sink.remove_combined_sink()

    def on_add_ladspa_effect(self, action):
        self.on_set_ladspa_effect(action.text(), self.get_pasink_name())

    def on_set_default_sink_triggered(self, action):
        if action:
            self.pa_sink.be_default_sink()

    def updateIcon(self):
        if self.isMuted():
            self.updateMutedInfo(True)
            self.mute.setMuted(True)
        else:
            self.updateMutedInfo(False)
            self.mute.setMuted(False)

    def updateMutedInfo(self, aBoolean):
        if self.isDefaultSink():
            self.muteInfo.emit(aBoolean)

    def update_label(self):
        if self.slider:
            self.slider.setBoldText(self.pa_sink.get_nice_title())
            self.set_name(self.pa_sink.get_nice_title())

## Drag and Drop Support

    def startDrag(self,event):
        drag = QDrag(event.widget())
        drag.setPixmap(self.mute.icon().pixmap(self.size().height(),self.size().height()))
        mimedata = QMimeData()
        liste = []
        liste.append(QUrl( "veromix://sink_index:"+str(int(self.index)) ))
        mimedata.setUrls(liste)
        drag.setMimeData(mimedata)
        #drag.setHotSpot(event.pos() - self.rect().topLeft())
        dropAction = drag.start(Qt.MoveAction)

    def dropEvent(self, dropEvent):
        uris = dropEvent.mimeData().urls()
        for uri in uris:
            if uri.scheme() == "veromix":
                if uri.host() == "sink_index" and uri.port() != self.index:
                    self.pa.create_combined_sink(self.index, uri.port())
                elif uri.host() == "sink_input_index":
                    self.pa.move_sink_input(uri.port(), self.index)

    def dragEnterEvent(self, event):
        uris = event.mimeData().urls()
        for uri in uris:
            if uri.scheme() == "veromix":
                 if uri.host() == "sink_index" and uri.port() == self.index:
                    return event.ignore()
        event.accept()
