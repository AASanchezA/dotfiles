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
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *
from PyKDE4.kdecore import *
from PyKDE4.plasma import *

class Label(Plasma.Label):
    volumeChanged = pyqtSignal(int)

    def __init__(self, parent=None, show_unit_value = False, unit_symbol="%"):
        self.text = ""
        self.bold_text = ""
        self.unit_value = -1
        self.unit_symbol = unit_symbol
        self.show_unit_value = show_unit_value
        Plasma.Label.__init__(self, parent)

    def setText(self, text):
        self.text = text
        self._set_text()

    def setBoldText(self,text):
        self.bold_text = text
        self._set_text()

    def _get_formated_unit_string(self):
        if self.show_unit_value and self.unit_value != -1:
            return str(self.unit_value).zfill(2) + self.unit_symbol + " "
        return ""

    def _set_text(self):
        Plasma.Label.setText(self, "<b>" + self._get_formated_unit_string() + self.bold_text + "</b> " + self.text)

    def update_unit_string(self,unit_value):
        self.unit_value = unit_value
        self._set_text()

    def setMinimum(self, value):
        pass

    def setMaximum(self, value):
        pass

    def update_with_info(self, info):
        pass

    def set_unit_value_visible(self, boolean):
        self.show_unit_value = boolean
        self._set_text()

class LabelSlider(Plasma.Slider):
    volumeChanged = pyqtSignal(int)

    def __init__(self, parent=None, show_unit_value=False, unit_symbol="%"):
        self.DELAY=  1
        self.text = ""
        self.bold_text = ""
        d =  datetime.timedelta(seconds=2)
        self.pulse_timestamp = datetime.datetime.now()  + d
        self.plasma_timestamp = datetime.datetime.now() + d
        Plasma.Slider.__init__(self)
        self.label = Label(self, show_unit_value, unit_symbol)
        self.label.setPos(0, -4)

        self.connect(self, SIGNAL("geometryChanged()"), self._resize_widgets)
        self.valueChanged.connect( self.on_slider_cb)

    def setMaximum(self, value, showticks=True):
        Plasma.Slider.setMaximum(self,value)
        if value > 100 and showticks:
            self.nativeWidget().setTickInterval(100)
            self.nativeWidget().setTickPosition(QSlider.TicksBelow)
        else:
            self.nativeWidget().setTickPosition(QSlider.NoTicks)

    def set_unit_value_visible(self, boolean):
        self.label.set_unit_value_visible(boolean)

    def _resize_widgets(self):
        w = self.size().width()
        self.label.setMinimumWidth(w)
        self.label.setMaximumWidth(w)
        # set abs position of label, respect fonts-size
        h = self.size().height()
        s = Plasma.Theme.defaultTheme().fontMetrics().height() + 2
        v = int ((h/2) - s)
        self.label.setPos(0,v)

    def setText(self, text):
        self.label.setText(text)

    def setBoldText(self,text):
        self.label.setBoldText(text)

    def setValueFromPlasma(self, value):
        if self.check_pulse_timestamp():
            self.update_plasma_timestamp()
            self.setValue(value)

    def setValue(self,value):
        Plasma.Slider.setValue(self,value)
        self.label.update_unit_string(value)

    def update_with_info(self, info):
        self.setValueFromPulse(info.get_volume())

    def setValueFromPulse(self, value):
        if self.check_plasma_timestamp():
            self.update_pulse_timestamp()
            self.setValue(value)

    def on_slider_cb(self, value):
        self.label.update_unit_string(value)
        if self.check_pulse_timestamp():
            self.update_plasma_timestamp()
            self.volumeChanged.emit(value)

    def set_focus(self):
        self.scene().setFocusItem(self, Qt.TabFocusReason)

# private
    def update_pulse_timestamp(self):
        self.pulse_timestamp = datetime.datetime.now()

    def update_plasma_timestamp(self):
        self.plasma_timestamp = datetime.datetime.now()

## testing
    def check_plasma_timestamp(self):
        now = datetime.datetime.now()
        return  (now - self.plasma_timestamp).seconds > self.DELAY

    def check_pulse_timestamp(self):
        now = datetime.datetime.now()
        return  (now - self.pulse_timestamp).seconds > self.DELAY

class VerticalSlider(LabelSlider):
    volumeChanged = pyqtSignal(int)

    def __init__(self):
        LabelSlider.__init__(self)
        self.label.setRotation(-90)
        self._resize_widgets()

    def _resize_widgets(self):
        h = self.size().height()
        self.label.setPos(-6, h)
        w = self.size().height()
        self.label.setMinimumWidth(w)
        self.label.setMaximumWidth(w)

class MeterSlider(QGraphicsWidget):
    volumeChanged = pyqtSignal(int)

    def __init__(self, show_unit_value = False, unit_symbol="%"):
        QGraphicsWidget.__init__(self)
        self.meter = None
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed,True))

        self.slider = LabelSlider(show_unit_value, unit_symbol)
        self.slider.setParent(self)
        self.slider.volumeChanged.connect(self.on_volume_changed)

        self.layout = QGraphicsLinearLayout(Qt.Vertical)
        self.layout.setContentsMargins(2,2,2,0)

        self.setLayout(self.layout)
        self.layout.addItem(self.slider)

        self.connect(self, SIGNAL("geometryChanged()"), self._resize_widgets)

    def create_meter(self):
        self.meter = Plasma.Meter(self)
        self.meter.setMeterType(Plasma.Meter.BarMeterHorizontal)
        self.meter.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed, True))
        self.meter.setZValue(0)
        if self.event_filter:
            self.meter.installEventFilter(self.event_filter)

    def on_volume_changed(self,val):
        self.volumeChanged.emit(val)
    def setOrientation(self, orient):
        self.slider.setOrientation(orient)
    def setMaximum(self, orient):
        self.slider.setMaximum(orient)
    def setMinimum(self, orient):
        self.slider.setMinimum(orient)
    def setText(self, text):
        self.slider.setText(text)
    def setBoldText(self,text):
        self.slider.setBoldText(text)
    def setValueFromPlasma(self, value):
        self.slider.setValueFromPlasma(value)
    def update_with_info(self, info):
        self.slider.update_with_info(info)
    def setValueFromPulse(self, value):
        self.slider.setValueFromPulse(value)
    def nativeWidget(self):
        return self.slider.nativeWidget()
    def set_unit_value_visible(self, boolean):
        self.slider.set_unit_value_visible(boolean)

    def _resize_widgets(self):
        if not self.meter:
            return

        meter_width = self.size().width()
        self.meter.setMinimumWidth(meter_width)
        self.meter.setMaximumWidth(meter_width)

        meter_height = Plasma.Theme.defaultTheme().fontMetrics().height()
        self.meter.setMinimumHeight(meter_height)
        self.meter.setMaximumHeight(meter_height)

        self.meter.setPos(0, int(self.size().height()/2))
        self.slider.setZValue(800)
        self.slider.label.setZValue(100)

    def toggle_meter(self):
        self.set_meter_visible((self.meter == None))

    def set_meter_value(self, value):
        if self.meter:
            self.meter.setValue(int(value))

    def set_meter_visible(self, aboolean):
        if aboolean:
            self.create_meter()
        else:
            if self.meter:
                self.meter.setParent(None)
                del self.meter
                self.meter = None
        self._resize_widgets()

    def installEventFilter(self, filter):
        self.event_filter = filter
        self.slider.installEventFilter(filter)
        self.slider.label.installEventFilter(filter)
        if self.meter:
            self.meter.installEventFilter(filter)
        QGraphicsWidget.installEventFilter(self, filter)

    def set_focus(self):
        self.slider.set_focus()
