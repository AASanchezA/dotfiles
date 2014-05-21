# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Nik Lutz <nik.lutz@gmail.com>
# Copyright (C) 2009 Harry Karvonen <harry.karvonen@gmail.com>
# Copyright (C) 2009 Paul W. Frields <stickster@gmail.com>
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
from .PulseClient import PulseClientCtypes
from .PulseVolume import PulseVolumeCtypes
from .PulseVolume import PulseVolume
from VeromixUtils import *

# This class contains all commons features from PulseSourceInputInfo and
# PulseSourceInfo
class PulseSource:
    def __init__(self, index, name, client):
        self.index  = int(index)
        self.name   = in_unicode(name)
        self.client = client
        self.isDefaultSource = False
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

    def printDebug(self):
        print("self.name:", self.name)
        print("self.index:", self.index)
        print("self.client:", self.client)
        return

    def set_has_monitor(self, aboolean):
        self.monitor_enabled = aboolean

    def has_monitor(self):
        return self.monitor_enabled

    def propDict(self):
        return {
            "name:": self.name,
            "index:": self.index ,
            "client:": self.client,
            "has_monitor" : str(self.has_monitor())}
################################################################################

class PulseSourceInfo(PulseSource):
    def __init__(self, pa_source_info):
        PulseSource.__init__(self,
                                 pa_source_info.index,
                                 pa_source_info.name,
                                 PulseClient("PulseSourceInfo"))
        self.mute =  pa_source_info.mute
        self.volume = PulseVolumeCtypes(pa_source_info.volume,pa_source_info.channel_map )

        self.description          = in_unicode(pa_source_info.description)
        self.sample_spec          = in_unicode(pa_source_info.sample_spec)
        self.channel_map          = in_unicode(pa_source_info.channel_map)
        self.owner_module         = in_unicode(pa_source_info.owner_module)
        self.monitor_of_sink      = in_unicode(pa_source_info.monitor_of_sink)
        self.monitor_of_sink_name = in_unicode(pa_source_info.monitor_of_sink_name)
        self.latency              = in_unicode(pa_source_info.latency)
        self.driver               = in_unicode(pa_source_info.driver)
        self.flags                = in_unicode(pa_source_info.flags)
        self.proplist             = pa_source_info.proplist
        self.n_ports              = int(pa_source_info.n_ports)
        self.ports = {}
        self.active_port = ""

        for x in range(self.n_ports):
            self.ports[in_unicode(pa_source_info.ports[x].contents.name)] = in_unicode(pa_source_info.ports[x].contents.description)

        if pa_source_info.active_port:
            self.active_port = in_unicode(pa_source_info.active_port.contents.name)

        #self.configured_latency   = pa_source_info.configured_latency
        self.proplist_string = in_unicode(pa_proplist_to_string(pa_source_info.proplist))
        self.proplist_dict = proplist_to_dict(self.proplist_string )

        return

    def propDict(self):
        aDict = {
            "description": self.description,
            "sample_spec": self.sample_spec ,
            "channel_map": self.channel_map,
            "owner_module":self.owner_module ,
            "monitor_of_sink":self.monitor_of_sink ,
            "monitor_of_sink_name":self.monitor_of_sink_name ,
            "latency":self.latency ,
            "driver":self.driver ,
            "flags":self.flags,
            "isdefault" : str(self.isDefaultSource),
            "has_monitor" : str(self.has_monitor())}
        aDict.update(self.proplist_dict)

        return assertEncoding(aDict)
    ###
    #
    # Define PROTOTYPE functions

    def unmuteStream(self, pulseInterface):
        pulseInterface.pulse_unmute_source(self.index)

        self.mute = 0
        return

    ###

    def muteStream(self, pulseInterface):
        pulseInterface.pulse_mute_source(self.index)

        self.mute = 1
        return

    ###

    def setVolume(self, pulseInterface, volume):
        pulseInterface.pulse_set_source_volume(self.index, volume)

        self.volume = volume
        return

    ###

    def printDebug(self):
        print("PulseSourceInfo")
        PulseSource.printDebug(self)
        print("self.mute:", self.mute)
        print("self.volume:", self.volume)
        print("self.description", self.description)
        print("self.sample_spec", self.sample_spec)
        print("self.channel_map", self.channel_map)
        print("self.owner_module", self.owner_module)
        print("self.monitor_of_sink", self.monitor_of_sink)
        print("self.monitor_of_sink_name", self.monitor_of_sink_name)
        print("self.latency", self.latency)
        print("self.driver", self.driver)
        print("self.flags", self.flags)
        #print "self.proplist", self.proplist
        print("self.configured_latency", self.configured_latency)
        return

    ###

    def __str__(self):
        return "ID: " + str(self.index) + ", Name: \"" + \
               self.name + "\""

    def updateDefaultSource(self, string):
        self.isDefaultSource = (self.name == string)

################################################################################

class PulseSourceOutputInfo(PulseSource):
    def __init__(self, pa_source_output_info):
        PulseSource.__init__(self,
                                 pa_source_output_info.index,
                                 pa_source_output_info.name,
                                 PulseClient("PulseSourceOutputInfo"))
        self.owner_module    = pa_source_output_info.owner_module
        self.client_id       = pa_source_output_info.client
        self.source          = in_unicode(pa_source_output_info.source)

        self.sample_spec     = pa_source_output_info.sample_spec
        self.channel_map     = pa_source_output_info.channel_map
        self.buffer_usec     = pa_source_output_info.buffer_usec
        self.source_usec     = None #pa_source_output_info.source_usec
        self.resample_method = in_unicode(pa_source_output_info.resample_method)
        self.driver          = pa_source_output_info.driver
        self.proplist        = pa_source_output_info.proplist
        self.proplist_string = in_unicode(pa_proplist_to_string(pa_source_output_info.proplist))
        self.proplist_dict = proplist_to_dict(self.proplist_string )

        return

    def propDict(self):
        aDict = self.proplist_dict

        aDict.update({
            "owner_module": self.owner_module,
            "client_id": self.client_id,
            "source": self.source ,
            "sample_spec": self.sample_spec,
            "channel_map":self.channel_map ,
            "buffer_usec":self.buffer_usec ,
            "source_usec":self.source_usec ,
            "driver":self.driver ,
            "resample_method":self.resample_method,
            "isdefault" : str(self.isDefaultSource),
            "has_monitor" : str(self.has_monitor())})
        return assertEncoding(aDict)


    ###

    def setClient(self, c):
        self.client = c

    ###

    def printDebug(self):
        print("PulseSourceOutputInfo")
        PulseSource.printDebug(self)

        print("self.owner_module:", self.owner_module)
        print("self.client_id:", self.client_id)
        print("self.source:", self.source)
        print("self.sample_spec:", self.sample_spec)
        print("self.channel_map:", self.channel_map)
        print("self.buffer_usec:", self.buffer_usec)
        print("self.source_usec:", self.source_usec)
        print("self.resample_method:", self.resample_method)
        print("self.driver:", self.driver)

    ###

    def __str__(self):
        if self.client:
            return "ID: " + str(self.index) + ", Name: \"" + \
                   self.name + "\", " + str(self.client)
        return "ID: " + str(self.index) + ", Name: \"" + \
               self.name + "\", "
