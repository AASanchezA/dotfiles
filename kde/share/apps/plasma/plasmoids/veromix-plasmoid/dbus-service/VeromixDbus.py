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
import sys
import dbus
import dbus.service

#from PulseAudio import *
from pulseaudio.PulseVolume import *


###
# The DBUS interface we offer
###
class VeromixDbus(dbus.service.Object):

    #interface = "org.veromix.pulseaudioservice"
    def __init__(self, pulseaudio, conn , object_path='/org/veromix/pulseaudio'):
        dbus.service.Object.__init__(self, conn, object_path)
        self.pulse = pulseaudio
        self.VERSION = 15

    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='')
    def veromix_startup(self):
        pass

## ----------------------------- source -----------------------------------------
    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='isba{ia{si}}a{ss}a{ss}s')
    def source_info(self, index,  name , mute, volume , dictProperties, ports, active_port):
        pass

    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='d')
    def source_remove(self, index ):
        pass

    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='id')
    def volume_meter_source(self, index,value ):
        pass

    @dbus.service.method("org.veromix.pulseaudio", in_signature='s', out_signature='')
    def set_default_source(self, index):
        self.pulse.pulse_set_default_source(index)

## ----------------------------- source output-----------------------------------------
    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='isa{ss}')
    def source_output_info(self, index,  name , dictProperties):
        pass

    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='i')
    def source_output_remove(self, index ):
        pass

    @dbus.service.method("org.veromix.pulseaudio", in_signature='ib', out_signature='')
    def source_mute(self, index, mute):
        self.pulse.pulse_source_mute(int(index), int(mute))

    @dbus.service.method("org.veromix.pulseaudio", in_signature='is', out_signature='')
    def source_port(self, index, portstr):
        self.pulse.pulse_set_source_port(int(index), portstr)

    @dbus.service.method("org.veromix.pulseaudio", in_signature='iai', out_signature='')
    def source_volume(self, index, vol):
        self.pulse.pulse_set_source_volume(index, PulseVolume(vol))

    @dbus.service.method("org.veromix.pulseaudio", in_signature='ii', out_signature='')
    def  move_source_output(self, index, output):
        self.pulse.pulse_move_source_output( index, output)

    @dbus.service.method("org.veromix.pulseaudio", in_signature='is', out_signature='')
    def toggle_monitor_of_source(self, source_index, named ):
        self.pulse.pulse_toggle_monitor_of_source( source_index, named)

## -----------------------------sink -----------------------------------------
    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='isba{ia{si}}a{ss}a{ss}s')
    def sink_info(self, index,  name , mute, volume , dictProperties, ports, active_port):
        pass

    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='i')
    def sink_remove(self, index ):
        pass

    @dbus.service.method("org.veromix.pulseaudio", in_signature='ib', out_signature='')
    def sink_mute(self, index, mute):
        self.pulse.pulse_sink_mute(int(index), int(mute))

    @dbus.service.method("org.veromix.pulseaudio", in_signature='is', out_signature='')
    def sink_port(self, index, portstr):
        self.pulse.pulse_set_sink_port(int(index), portstr)

    @dbus.service.method("org.veromix.pulseaudio", in_signature='iai', out_signature='')
    def sink_volume(self, index, vol):
        self.pulse.pulse_set_sink_volume(int(index), PulseVolume(vol))

    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='id')
    def volume_meter_sink(self, index,value ):
        pass

    @dbus.service.method("org.veromix.pulseaudio", in_signature='is', out_signature='')
    def toggle_monitor_of_sink(self, sink_index,named ):
        self.pulse.pulse_toggle_monitor_of_sink( sink_index, named)

    @dbus.service.method("org.veromix.pulseaudio", in_signature='s', out_signature='')
    def set_default_sink(self, index):
        self.pulse.pulse_set_default_sink(index)

    @dbus.service.method("org.veromix.pulseaudio", in_signature='ii', out_signature='')
    def create_combined_sink(self, fist_sink_index, second_sink_index):
        self.pulse.create_combined_sink(fist_sink_index, second_sink_index)

## -----------------------------sink input-----------------------------------------
    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='isba{ia{si}}a{ss}')
    def sink_input_info(self, index,  name , mute, volume , dictProperties):
        pass

    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='i')
    def sink_input_remove(self, index ):
        pass

    @dbus.service.method("org.veromix.pulseaudio", in_signature='i', out_signature='')
    def sink_input_kill(self, index):
        self.pulse.pulse_sink_input_kill(int(index))

    @dbus.service.method("org.veromix.pulseaudio", in_signature='ib', out_signature='')
    def sink_input_mute(self, index, mute):
        self.pulse.pulse_sink_input_mute(int(index), int(mute))

    @dbus.service.method("org.veromix.pulseaudio", in_signature='iai', out_signature='')
    def sink_input_volume(self, index, vol):
        v = PulseVolume(vol)
        self.pulse.pulse_set_sink_input_volume( index , v)

    @dbus.service.method("org.veromix.pulseaudio", in_signature='ii', out_signature='')
    def  move_sink_input(self, index, output):
        self.pulse.pulse_move_sink_input( index, output)

    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='id')
    def volume_meter_sink_input(self, index,value ):
        pass

    @dbus.service.method("org.veromix.pulseaudio", in_signature='iis', out_signature='')
    def toggle_monitor_of_sinkinput(self, sink_input_index, sink_index, named ):
        self.pulse.pulse_toggle_monitor_of_sinkinput( sink_input_index, sink_index, named)

## ----------------------------- card info -----------------------------------------

    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='isa{ss}sa{sa{ss}}')
    def card_info(self, index,  name , properties, active_profile_name , profiles):
        pass

    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='i')
    def card_remove(self, index ):
        pass

    @dbus.service.method("org.veromix.pulseaudio", in_signature='is', out_signature='')
    def set_card_profile(self, index, value):
        self.pulse.pulse_set_card_profile(index, value)

## ----------------------------- Modules -----------------------------------------

    @dbus.service.signal(dbus_interface="org.veromix.notification", signature='issss')
    def module_info(self, index, name, argument, n_used, auto_unload):
        pass

    @dbus.service.method("org.veromix.pulseaudio", in_signature='iis', out_signature='')
    def set_ladspa_sink(self, sink_index, module_index, parameters):
        self.pulse.set_ladspa_sink(sink_index, module_index, parameters)

    @dbus.service.method("org.veromix.pulseaudio", in_signature='i', out_signature='')
    def remove_ladspa_sink(self, sink_index):
        self.pulse.remove_ladspa_sink(sink_index)

    @dbus.service.method("org.veromix.pulseaudio", in_signature='i', out_signature='')
    def remove_combined_sink(self, sink_index):
        self.pulse.remove_combined_sink(sink_index)

## ----------------------------- generic -----------------------------------------

    @dbus.service.method("org.veromix.pulseaudio", in_signature='', out_signature='')
    def requestInfo(self):
        self.pulse.requestInfo()

    @dbus.service.method("org.veromix.pulseaudio", in_signature='', out_signature='i')
    def veromix_service_version(self):
        return self.VERSION

    @dbus.service.method("org.veromix.pulseaudio", in_signature='b', out_signature='')
    def set_autostart_meters(self, aboolean):
        self.pulse.set_autostart_meters(aboolean)

    @dbus.service.method("org.veromix.pulseaudio", in_signature='', out_signature='')
    def veromix_service_quit(self):
        sys.exit(0)
