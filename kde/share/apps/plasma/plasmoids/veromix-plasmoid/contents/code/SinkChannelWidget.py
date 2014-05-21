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

from PyKDE4.plasma import Plasma
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import *

from LabelSlider import LabelSlider

class SinkChannelWidget(QGraphicsWidget):

    def __init__(self, veromix, sink):
        QGraphicsWidget.__init__(self)
        self.veromix = veromix
        self.sink = sink
        self.sliders = []
        self.text = ""
        self.bold_text = ""
        self.init()

    def init(self):
        self.init_arrangement()
        self.create_channel_sliders()
        self.compose_arrangement()

    def compose_arrangement(self):
        self.setContentsMargins(0,0,0,0)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addItem(self.label)
        self.layout.addItem(self.slider_widget)
        self.adjustSize()

    def init_arrangement(self):
        self.layout = QGraphicsLinearLayout(Qt.Vertical)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed, True))
        self.layout.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed, True))
        self.setLayout(self.layout)

        self.label = Plasma.Label()
        self.label.setPreferredHeight(self.sink.mute.size().height())
        self.label.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed, True))

    def create_channel_sliders(self):
        self.slider_layout = QGraphicsLinearLayout(Qt.Vertical)
        self.slider_layout.setContentsMargins(0,2,0,0)

        self.slider_widget = QGraphicsWidget()
        self.slider_widget.setLayout(self.slider_layout)
        self.slider_widget.setContentsMargins(0,0,0,0)

    def create_sliders(self):
        for channel in self.sink.pa_sink.getChannels():
            slider = LabelSlider()
            slider.setOrientation(Qt.Horizontal)
            slider.setText(channel.get_name())
            slider.setMaximum(self.veromix.get_max_volume_value())
            slider.setValue(channel.get_volume())
            slider.volumeChanged.connect(self.on_slider_cb)
            self.sliders.append(slider)
            self.slider_layout.addItem(slider)
            slider.installEventFilter(self.event_filter)

    def remove_sliders(self):
        for slider in self.sliders:
            self.slider_layout.removeItem(slider)
            del slider
        del self.sliders
        self.sliders = []

## FIXME
    def setText(self, text):
        if text:
            self.text = text
        self.label.setText( "<b>"+self.bold_text + "</b> " + self.text)

    def setBoldText(self,text):
        if text:
            self.bold_text = text
        self.setText(self.text)

    def update_with_info(self, info):
        self.set_slider_values()

    def set_slider_values(self):
        channels = self.sink.pa_sink.getChannels()
        if len(channels) != len(self.sliders):
            self.remove_sliders()
            self.create_sliders()
        for i in range(0,len(channels)):
            name = channels[i].get_name()
            if name != "None":
                self.sliders[i].setBoldText("")
                self.sliders[i].setText(name)
            self.sliders[i].setValueFromPulse(channels[i].get_volume())

    def on_slider_cb(self, value):
        vol = []
        for slider in self.sliders:
            vol.append(slider.value())
            slider.update_plasma_timestamp()
        self.sink.set_channel_volumes(vol)

    def setMaximum(self, value):
        for slider in self.sliders:
            slider.setMaximum(value)

    def wheelEvent(self, event):
        # dont touch the sliders, they will get the new values
        # via the pa-callback
        # else we get infinite loops
        self.sink.on_step_volume(event.delta() > 0)

    def installEventFilter(self, filter):
        if filter:
            self.event_filter = filter
        for slider in self.sliders:
            slider.installEventFilter(filter)
        self.label.installEventFilter(filter)
        self.slider_widget.installEventFilter(filter)
        QGraphicsWidget.installEventFilter(self,filter)

    def set_focus(self):
        # FIXME
        self.sliders[0].set_focus()
