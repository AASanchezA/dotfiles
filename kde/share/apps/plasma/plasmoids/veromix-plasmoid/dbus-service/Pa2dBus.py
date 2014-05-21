#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Nik Lutz <nik.lutz@gmail.com>
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

import signal
import datetime
import dbus
import dbus.service

#from PyQt4.QtCore import QObject
#from PyQt4.QtCore import SIGNAL

#from PyQt4 import QtCore
from VeromixUtils import *

###
# Pass info/signals from PA to DBUS
###
class Pa2dBus():

    def __init__(self, veromixdbus, pulseaudio):
        self.dbus = veromixdbus
        self.pulse = pulseaudio
        self.LIMIT_SEND_METER_ENABLED = False
        self.METER_SEND_MSECS = 100000 #micro
        self.last_volume_meter_send = datetime.datetime.now()
        self.last_source_meter_send = datetime.datetime.now()
#        self.connect(self.pulse, SIGNAL("sink_info(PyQt_PyObject)"), self.on_sink_info)
#        self.connect(self.pulse, SIGNAL("sink_remove(int)"), self.on_remove_sink)

#        self.connect(self.pulse, SIGNAL("sink_input_info(PyQt_PyObject)"), self.on_sink_input_info)
#        self.connect(self.pulse, SIGNAL("sink_input_remove(int)"), self.on_remove_sink_input)

#        self.connect(self.pulse, SIGNAL("source_info(PyQt_PyObject)"), self.on_source_info)
#        self.connect(self.pulse, SIGNAL("source_remove(int)"), self.on_remove_source)

#        self.connect(self.pulse, SIGNAL("source_output_info(PyQt_PyObject)"), self.on_source_output_info)
#        self.connect(self.pulse, SIGNAL("source_output_remove(int)"), self.on_remove_source_output)

#        self.connect(self.pulse, SIGNAL("volume_meter_sink_input(int, float )"), self.on_volume_meter_sink_input)
#        self.connect(self.pulse, SIGNAL("volume_meter_sink(int, float )"), self.on_volume_meter_sink)
#        self.connect(self.pulse, SIGNAL("volume_meter_source(int, float )"), self.on_volume_meter_source)

#        self.connect(self.pulse, SIGNAL("card_info(PyQt_PyObject)"), self.on_card_info)
#        self.connect(self.pulse, SIGNAL("card_remove(int)"), self.on_remove_card)

#        self.connect(self.pulse, SIGNAL("module_info(int, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.on_module_info)

    def on_source_info(self, sink):
        index =   int(sink.index)
        name = in_unicode(sink.name)
        muted = (sink.mute == 1)
        volume = sink.volume.getVolumes()
        active_port = sink.active_port
        ports = sink.ports
        props = sink.propDict()
        if "device.class" in props.keys() and props["device.class"]  == "monitor":
            return
        self.dbus.source_info(index, name, muted, volume, props, ports, active_port)

    def on_source_output_info(self, sink):
        index =  int(sink.index)
        name = in_unicode(sink.name)
        if sink.resample_method != "peaks":
            self.dbus.source_output_info(index, name, sink.propDict())

    def on_sink_input_info(self, sink):
        index =   int(sink.index)
        name = in_unicode(sink.name)
        muted = (sink.mute == 1)
        volume = sink.volume.getVolumes()
        self.dbus.sink_input_info(index, name, muted, volume, sink.propDict())

    def on_sink_info(self, sink):
        index =   int(sink.index)
        name = in_unicode(sink.name)
        muted = (sink.mute == 1)
        volume = sink.volume.getVolumes()
        self.dbus.sink_info(index, name, muted, volume, sink.propDict(), sink.ports, sink.active_port)

    def on_card_info(self, card_info):
        self.dbus.card_info(card_info.index, card_info.name, card_info.properties(), card_info.active_profile_name(), card_info.profiles_dict())

    def on_remove_card(self, index):
        self.dbus.card_remove(index)

    def on_remove_sink(self, index):
        self.dbus.sink_remove(index)

    def on_remove_sink_input(self, index):
        self.dbus.sink_input_remove(index)

    def on_remove_source(self, index):
        self.dbus.source_remove(int(index))

    def on_remove_source_output(self, index):
        self.dbus.source_output_remove(int(index))

    def on_volume_meter_sink_input(self, index, level):
        if level == level:
            if self.LIMIT_SEND_METER_ENABLED:
                now = datetime.datetime.now()
                # FIXME limit dbus spam but this solution could always prevent the same source  from transmitting
                if (now - self.last_volume_meter_send).microseconds > self.METER_SEND_MSECS :
                    self.last_volume_meter_send = now
                    self.dbus.volume_meter_sink_input(int(index),level)
            else:
                self.dbus.volume_meter_sink_input(int(index),level)

    def on_volume_meter_sink(self, index, level):
        if level == level:
            if self.LIMIT_SEND_METER_ENABLED:
                now = datetime.datetime.now()
                # FIXME limit dbus spam but this solution could always prevent the same source  from transmitting
                if (now - self.last_volume_meter_send).microseconds > self.METER_SEND_MSECS :
                    self.last_volume_meter_send = now
                    self.dbus.volume_meter_sink(int(index),level)
            else:
                self.dbus.volume_meter_sink(int(index),level)

    def on_volume_meter_source(self, index, level):
        if level == level:
            if self.LIMIT_SEND_METER_ENABLED:
                now = datetime.datetime.now()
                # FIXME limit dbus spam but this solution could always prevent the same source  from transmitting
                if (now - self.last_source_meter_send).microseconds > self.METER_SEND_MSECS :
                    self.last_source_meter_send = now
                    self.dbus.volume_meter_source(int(index),level)
            else:
                self.dbus.volume_meter_source(int(index),level)

    def on_module_info(self, index, name, argument, n_used, auto_unload):
        self.dbus.module_info(index, in_unicode(name), in_unicode(argument), in_unicode(n_used), in_unicode(auto_unload))
