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
from ctypes import *

from .PulseClient import PulseClient
from .PulseVolume import PulseVolumeCtypes

class PulseStream:
    def __init__(self, context, name, sample_spec, channel_map):
        self.context = context
        self.name = name
        self.sample_spec = sample_spec
        self.channel_map = channel_map
        self.data = None
        self.size = None
        return

    def connect_record(self, source):

                 #pa_stream_connect_record(pa_stream, str(monitor_index), attr, 10752)
        retval = pa_stream_connect_record(self,
                                          source.name,
                                          None, # buffer_attr
                                          0) # flags
        if retval != 0:
            raise Exception("Couldn't do connect_record()")


    def peek(self, pulseInterface):
        pa_stream_peek(self, data, size)

    def disconnect(self):
        retval = pa_stream_disconnect(self)
        if retval != 0:
            raise Exception("Couldn't do disconnect()")
