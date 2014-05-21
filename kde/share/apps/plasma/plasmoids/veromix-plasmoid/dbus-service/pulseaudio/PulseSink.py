# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Nik Lutz <nik.lutz@gmail.com>
# Copyright (C) 2009 Harry Karvonen <harry.karvonen@gmail.com>
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

from .lib_pulseaudio import *

from .PulseClient import PulseClient
from .PulseVolume import PulseVolumeCtypes
from VeromixUtils import *

# This class contains all commons features from PulseSinkInputInfo and
# PulseSinkInfo


def todict(obj):
    data = {}
    for key, value in obj.__dict__.items():
        try:
            data[key] = todict(str(value))
        except AttributeError:
            data[key] = value
    return data


class PulseSink:

    def __init__(self, index, name, mute, volume, client):
        self.index  = int(index)
        self.name   = in_unicode(name)
        self.mute   = mute
        self.volume = volume
        self.client = client
        self.isDefaultSink = False
        self.default_sink_name = ""
        self.monitor_enabled = False
        return

    # PROTOTYPE
    def unmuteStream(self):
        raise Exception("ABSTRACT METHOD CALLED")
        return

    # PROTOTYPE
    def muteStream(self):
        raise Exception("ABSTRACT METHOD CALLED")
        return

    # PROTOTYPE
    def setVolume(self):
        raise Exception("ABSTRACT METHOD CALLED")
        return

    def asDict(self):
        return todict(self)

    def propDict(self):
        return {"pulsesink":"pulsesink"}

    def updateDefaultSink(self, string):
        self.isDefaultSink = (self.name == in_unicode(string))
        self.default_sink_name = in_unicode(string)

    def set_has_monitor(self, aboolean):
        self.monitor_enabled = aboolean

    def has_monitor(self):
        return self.monitor_enabled

    def printDebug(self):
        print("self.index:", self.index)
        print("self.name:", in_unicode(self.name))
        print("self.mute:", self.mute)
        print("self.volume:", self.volume)
        print("self.client:", self.client)
        return

################################################################################

class PulseSinkInfo(PulseSink):
    def __init__(self, pa_sink_info):
        PulseSink.__init__(self, pa_sink_info.index,
                                 pa_sink_info.name,
                                 pa_sink_info.mute,
                                 PulseVolumeCtypes(pa_sink_info.volume, pa_sink_info.channel_map),
                                 PulseClient("Selected Sink"))
        self.description         = in_unicode(pa_sink_info.description)
        self.sample_spec         = in_unicode(pa_sink_info.sample_spec)
        self.channel_map         = in_unicode(pa_sink_info.channel_map)
        self.owner_module        = int(pa_sink_info.owner_module)
        self.monitor_source      = in_unicode(pa_sink_info.monitor_source)
        self.monitor_source_name = in_unicode(pa_sink_info.monitor_source_name)
        self.latency             = int(pa_sink_info.latency)
        self.driver              = in_unicode(pa_sink_info.driver)
        self.flags               = in_unicode(pa_sink_info.flags)
        self.proplist            = pa_sink_info.proplist
        self.active_port         = ""
        self.ports = {}

        for x in range(pa_sink_info.n_ports):
            self.ports[in_unicode(pa_sink_info.ports[x].contents.name)] = in_unicode(pa_sink_info.ports[x].contents.description)

        if(pa_sink_info.active_port):
            self.active_port         = in_unicode(pa_sink_info.active_port.contents.name)
        #self.configured_latency  = pa_sink_info.configured_latency
        self.device_name = in_unicode(pa_proplist_gets(pa_sink_info.proplist, as_p_char("device.description")))
        self.proplist_string =  in_unicode( pa_proplist_to_string(pa_sink_info.proplist))
        self.proplist_dict = proplist_to_dict(self.proplist_string )
        return


    def propDict(self):
        dict = {
                "description":  self.description ,
                 # self.sample_spec
                 #self.channel_map
                 "owner_module": str(self.owner_module),
                 "monitor_source" :     str(self.monitor_source),
                  "monitor_source_name" : self.monitor_source_name,
                  "latency" : str(self.latency),
                  "driver" : str(self.driver) ,
                  "flags" : str(self.flags) ,
                   "device_name" : self.device_name,
                   "isdefault" : str(self.isDefaultSink),
                   "default_sink_name" : str(self.default_sink_name),
                   "has_monitor" : str(self.has_monitor())
           }
        dict.update(self.proplist_dict)
        return dict

    def asDict(self):
        obj = todict(self)
        for key in ["sample_spec", "channel_map" ,"proplist"]:
            if key in list(obj.keys()):
                del obj[key]
        return assertEncoding(obj)
        #return obj

    ###
    #
    # Define PROTOTYPE functions

    def unmuteStream(self, pulseInterface):
        pulseInterface.pulse_unmute_sink(self.index)
        self.mute = 0
        return

    ###

    def muteStream(self, pulseInterface):
        pulseInterface.pulse_mute_sink(self.index)
        self.mute = 1
        return

    ###

    def setVolume(self, pulseInterface, volume):
        pulseInterface.pulse_set_sink_volume(self.index, volume)
        self.volume = volume
        return

    ###
    def asDict(self):
        return self.propDict()

    def printDebug(self):
        print("PulseSinkInfo")
        PulseSink.printDebug(self)
        print("self.description", self.description)
        print("self.sample_spec", self.sample_spec)
        print("self.channel_map", self.channel_map)
        print("self.owner_module", self.owner_module)
        print("self.monitor_source", self.monitor_source)
        print("self.monitor_source_name", self.monitor_source_name)
        print("self.latency", self.latency)
        print("self.driver", self.driver)
        print("self.flags", self.flags)
        print("self.proplist", self.proplist)
        #print "self.configured_latency", self.configured_latency
        return

    ###

    def __str__(self):
        return "ID: " + str(self.index) + ", Name: \"" + \
               self.name + "\""

################################################################################

class PulseSinkInputInfo(PulseSink):
    def __init__(self, pa_sink_input_info):
        PulseSink.__init__(self, pa_sink_input_info.index,
                                 pa_sink_input_info.name,
                                 pa_sink_input_info.mute,
                                 PulseVolumeCtypes(pa_sink_input_info.volume, pa_sink_input_info.channel_map),
                                 PulseClient("Unknown client"))
        self.owner_module    = in_unicode(pa_sink_input_info.owner_module)
        self.client_id       = int(pa_sink_input_info.client)
        self.sink            = int(pa_sink_input_info.sink)
        self.sample_spec     = in_unicode(pa_sink_input_info.sample_spec)
        self.channel_map     = in_unicode(pa_sink_input_info.channel_map)
        self.monitor_index   =  int(pa_sink_input_info.monitor_index)
        self.buffer_usec     = int(pa_sink_input_info.buffer_usec)
        self.sink_usec       = int(pa_sink_input_info.sink_usec)
        self.resample_method = in_unicode(pa_sink_input_info.resample_method)
        self.driver          = in_unicode(pa_sink_input_info.driver)
        self.proplist        = pa_sink_input_info.proplist

        self.proplist_string =  in_unicode( pa_proplist_to_string(pa_sink_input_info.proplist))
        self.proplist_dict = proplist_to_dict(self.proplist_string )
        self.app = in_unicode(pa_proplist_gets(pa_sink_input_info.proplist, as_p_char("application.name")))
        self.app_icon = in_unicode(pa_proplist_gets(pa_sink_input_info.proplist, as_p_char("application.icon_name")))
        if self.app and self.app.find("ALSA") == 0:
            self.app = in_unicode(pa_proplist_gets(pa_sink_input_info.proplist, as_p_char("application.process.binary")))
        return

    def propDict(self):
        adict = {
                "index" : str(self.index),
                "name" : in_unicode(self.name),
                "owner_module" : str(self.owner_module),

                "client_id" : str(self.client_id ) ,

                "sink" : str(self.sink),
                "sample_spec" : str(self.sample_spec),
                "channel_map" : str(self.channel_map),

                #"volume"
               "buffer_usec" : str(self.buffer_usec),
               "sink_usec" : str(self.sink_usec),
               "resample_method" : str(self.resample_method),
               "driver" : str(self.driver),
               #"mute"
               #"monitor_index" : str(self.monitor_index),

               "app" : str(self.app),
               "app_icon" : str(self.app_icon),
               "isdefault" : str(self.isDefaultSink),
               "has_monitor" : str(self.has_monitor())
               #"proplist" : str(self.proplist_string)
                }
        adict.update(self.proplist_dict)
        for key in ["sample_spec", "channel_map" ,"application.process.session_id"]:
            if key in list(adict.keys()):
                del adict[key]
        #print adict
        return assertEncoding(adict)
        #return adict

    ###

    def setClient(self, c):
        self.client = c

    ###
    #
    # Define PROTOTYPE functions

    def unmuteStream(self, pulseInterface):
        pulseInterface.pulse_unmute_stream(self.index)

        self.mute = 0
        return

    ###

    def muteStream(self, pulseInterface):
        pulseInterface.pulse_mute_stream(self.index)

        self.mute = 1
        return

    ###

    def setVolume(self, pulseInterface, volume):
        pulseInterface.pulse_set_sink_input_volume(self.index, volume)

        self.volume = volume
        return

    ###

    def printDebug(self):
        print("PulseSinkInputInfo")
        PulseSink.printDebug(self)

        print("self.owner_module:", self.owner_module)
        print("self.client_id:", self.client_id)
        print("self.sink:", self.sink)
        print("self.sample_spec:", self.sample_spec)
        print("self.channel_map:", self.channel_map)
        print("self.buffer_usec:", self.buffer_usec)
        print("self.sink_usec:", self.sink_usec)
        print("self.resample_method:", self.resample_method)
        print("self.driver:", self.driver)

    ###

    def __str__(self):
        if self.client:
            return "ID: " + str(self.index) + ", Name: \"" + \
                   str(self.name) + "\", mute: " + str(self.mute) + ", " + str(self.client)
        return "ID: " + str(self.index) + ", Name: \"" + \
               str(self.name) + "\", mute: " + str(self.mute)
