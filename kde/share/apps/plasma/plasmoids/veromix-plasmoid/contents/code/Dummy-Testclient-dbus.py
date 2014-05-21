#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import sys
import dbus
import dbus.mainloop.qt

from PyQt4.QtCore import *
import signal

## ps -ef | grep test-dbus  | grep -v grep  | awk '{ print $2 }' | xargs -n 1 kill

class PulseAudioDBus(QObject):

    #def __init__(self, sessionBus):
        #QObject.__init__(self)
        #self.call_manager_obj = sessionBus.get_object("org.veromix.pulseaudioservice","/org/veromix/pulseaudio")
        #self.call_manager = dbus.Interface(self.call_manager_obj, dbus_interface='org.veromix.notification' )
        #self.connectToSignals()

    #def connectToSignals(self):
        #self.call_manager.connect_to_signal("sink_info", self.sink_info)
        ##self.call_manager.connect_to_signal("incomingCall", self.incomingCall)
        ##self.call_manager.connect_to_signal("callStateChanged", self.callStateChanged)


    def __init__(self):
        bus = dbus.SessionBus()
        pa_obj  = bus.get_object("org.veromix.pulseaudioservice","/org/veromix/pulseaudio")
        interface = dbus.Interface(pa_obj,dbus_interface="org.veromix.notification")
        interface.connect_to_signal("sink_input_info", self.sink_input_info)
        interface.connect_to_signal("sink_info", self.sink_info)
        interface.connect_to_signal("sink_input_remove", self.sink_input_remove)
        interface.connect_to_signal("sink_remove", self.sink_remove)


    def sink_input_info(self,   index,   name,  muted  , volume , client_index,client_name, props):
        print "sink input signal: " ,  index,   name,  muted  , volume , client_index,client_name, props
        print ""

    def sink_info(self,  index,   name,  muted  , volume , client_index,client_name, props):
        print "sink signal: " ,  index,   name,  muted  , volume , client_index,client_name, props
        print ""

    def sink_input_remove(self, index):
        print "sink input remove signal: " ,  index

    def sink_remove(self, index):
        print "sink remove signal: " ,  index

    def pulse_set_sink_input_volume(self, index, vol):
        pass

    def pulse_sink_mute(self, index, mute):
        pass

    def pulse_set_sink_volume(self, index, vol):
        pass

    def pulse_sink_mute(self, index, mute):
        pass

if __name__ == '__main__':
    print 'Entering loop'
    app=QCoreApplication(sys.argv)
    mainloop=dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    bus = dbus.SessionBus()
    obj = PulseAudioDBus()
    app.exec_()
