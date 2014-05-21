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
import math
from VeromixUtils import *

# This contains all basic volume features
class PulseVolume:
    def __init__(self, vol, channels):
        self.channels = channels
        if vol > 100 or vol < 0:
            print("WARNING: Volume is invalid!")
            vol = 0
        self.values   = [vol] * self.channels
        return

    def __init__(self, values):
        self.channels = len(values)
        self.values   = values
        return

    ##############################
    #
    # Type conversions
    #
    #def fromCtypes(self, pa_cvolume):
    #  self.channels = pa_cvolume.channels
    #  self.values   = map(lambda x: (math.ceil(float(x) * 100 / PA_VOLUME_NORM)),
    #                      pa_cvolume.values[0:self.channels])
    #  return self

    def toCtypes(self):
        ct = struct_pa_cvolume()
        ct.channels = self.channels
        for x in range(0, self.channels):
            ct.values[x] = int((self.values[x] * PA_VOLUME_NORM) / 100)
        return ct

    def toCtypes2(self, num):
        ct = struct_pa_cvolume()
        ct.channels = num
        for x in range(0, num):
            ct.values[x] = (self.values[x] * PA_VOLUME_NORM) / 100
        return ct

    ###

    def printDebug(self):
        print("PulseVolume")
        print("self.channels:", self.channels)
        print("self.values:", self.values)
        #print "self.proplist:", self.proplist

    ###

    def incVolume(self, vol):
        "Increment volume level (mono only)"
        vol += sum(self.values) / len(self.values)
        vol = int(vol)
        if vol > 100:
            vol = 100
        elif vol < 0:
            vol = 0
        self.setVolume(vol)
        return

    ###

    def setVolume(self, vol, balance = None):
        if not balance:
            self.values = [vol] * self.channels
        else:
            self.values[balance] = vol
        return

    ###

    def getVolume(self):
        "Return mono volume"
        return int(sum(self.values) / len(self.values))

    ###

    def __str__(self):
        return "Channels: " + str(self.channels) + \
               ", values: \"" + str([str(x) + "%" for x in self.values]) + "\""

################################################################################

class PulseVolumeCtypes(PulseVolume):
    def __init__(self, pa_cvolume, pa_channel_map):
        self.channels = pa_cvolume.channels
        self.channel_map = pa_channel_map
        self.values   = [(math.ceil(float(x) * 100 / PA_VOLUME_NORM)) for x in pa_cvolume.values[0:self.channels]]
        return

    def getVolumes(self):
        vol = {}
        for i in range(0, self.channels):
            key = pa_channel_position_to_pretty_string(self.channel_map.map[i])
            entry = {}
            entry[in_unicode(key)] = self.values[i]
            vol[i] = entry
        return vol
