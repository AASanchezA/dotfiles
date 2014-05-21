# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 Nik Lutz <nik.lutz@gmail.com>
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

import signal, os, datetime, dbus
#from veromixcommon.PulseProxyObjects import *

##

class MediaPlayer():

    Stopped, Playing, Paused, NA = list(range(4))

    def __init__(self):
        self._state = MediaPlayer.NA
        self._position = 0
        self._length = 0
        self._artwork = None
        self._cover_string = ""
        self._last_playing_icon = None
        self._fetch_extended_info = False
        self.last_position_change = datetime.datetime.now()

    def init_connection(self):
        pass

    def disconnect(self):
        pass

    def state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def name(self):
        return None

    def play(self):
        pass

    def pause(self):
        pass

    def next_track(self):
        pass

    def prev_track(self):
        pass

    def seek(self, position):
        pass

    def length(self):
        return self._length

    def set_length(self, length):
        self._length = length

    def position(self):
        return self._position

    def set_position(self, position):
        self._position = position

    def artwork(self):
        return self._artwork

    def set_artwork(self, artwork):
        self._artwork = artwork

    def get_application_name(self):
        name = self.name()
        if str(name).find("org.mpris.MediaPlayer2.")  == 0:
            return name[23:]
        if str(name).find("org.mpris.")  == 0:
            return name[10:]
        return name

    def fetch_extended_info(self):
        return self._fetch_extended_info

    def set_fetch_extended_info(self, boolean):
        self._fetch_extended_info = boolean

    def is_nowplaying_player(self):
        return False

    def is_mpris2_player(self):
        return False

    def signal_data_updated(self):
        pass

## Abstract !!

    def url_path_of(self, string):
        pass

    def trigger_timer_callback(self, timeout, function):
        pass

    def create_pixmap(self, val):
        pass

class Mpris2MediaPlayer(MediaPlayer):
    def __init__(self,name, dbus_proxy):
        MediaPlayer.__init__(self)
        self._name = name
        self._dbus_proxy = dbus_proxy
        self._seek_position = 0
        self._timer_running = False

    def init_connection(self):
        self.connect_mpris2()

    def get_index(self):
        return self.name()

    def name(self):
        return self._name

    def play(self):
        self._dbus_proxy.nowplaying_play(self.name())

    def pause(self):
        self._dbus_proxy.nowplaying_pause(self.name())

    def next_track(self):
        self._dbus_proxy.nowplaying_next(self.name())

    def prev_track(self):
        self._dbus_proxy.nowplaying_prev(self.name())

    def seek(self, position):
        self.schedule_set_mpris2_position(position)

    def connect_mpris2(self):
        if self._dbus_proxy:
            self._dbus_proxy.connect_mpris2_player(self.on_mpris2_properties_changed, str(self.name()) )
            self.poll_dbus_info()

    def set_fetch_extended_info(self, boolean):
        MediaPlayer.set_fetch_extended_info(self, boolean)
        if boolean:
            self.poll_dbus_info()

    def poll_dbus_info(self):
        if not self._dbus_proxy:
            return
        properties = {}

        try:
            # Once connected we get notified via dbus about changes - but initially we fetch them manually
            properties[dbus.String("PlaybackStatus")] =self._dbus_proxy.mpris2_get_playback_status(self.name())
            properties[dbus.String("Metadata")] = self._dbus_proxy.mpris2_get_metadata(self.name())
            self.on_mpris2_properties_changed(None, properties, None)
            self.fetch_position()
        except:
            pass

    def on_mpris2_properties_changed(self, interface, properties, signature):
        changed = False

        if type(properties) == type(dbus.String("")):
            return
        if dbus.String("PlaybackStatus") in list(properties.keys()):
            status = properties[dbus.String("PlaybackStatus")]
            old_state = self.state()
            if status == 'Playing':
                self.set_state(MediaPlayer.Playing)
            else:
                 self.set_state(MediaPlayer.Paused)
            if old_state != self.state():
                changed = True

        if dbus.String("Metadata") in list(properties.keys()):
            metadata = properties[dbus.String("Metadata")]
            if type(metadata) == type(dbus.String("")):
                return
            if type(metadata) == type(dbus.Struct([""])):
                #deadbeef fallback
                metadata = metadata[0]
            #self.mpris2_trackid = metadata[dbus.String("mpris:trackid")]
            if dbus.String("mpris:artUrl") in list(metadata.keys()):
                val = self.url_path_of(str(metadata[dbus.String("mpris:artUrl")]))
                if val != self._cover_string:
                    changed = True
                    if (os.path.isfile(val)):
                       self.set_artwork(self.create_pixmap(val))
                    else:
                        self.set_artwork(None)
                    self._cover_string = val

            if dbus.String("mpris:length") in list(metadata.keys()):
                length = metadata[dbus.String("mpris:length")] / 1000000
                if length != self.length():
                    changed = True
                    self.set_length(length)
        if changed:
            self.signal_data_updated()

    def fetch_position(self):
        if self.fetch_extended_info():
            changed = False
            pos = self._dbus_proxy.mpris2_get_position(self.name())
            position = pos / 1000000
            if position != self.position() and position <= self.length():
                changed = True
                self.set_position(position)
            if changed:
                self.signal_data_updated()
            self.trigger_timer_callback(1500, self.fetch_position)

    def is_mpris2_player(self):
        return True

    # Don't flood players while dragging the slider.
    # Update the position at most every 500ms
    def schedule_set_mpris2_position(self, value=0):
        # FIXME
        now = datetime.datetime.now()
        time =  (now - self.last_position_change ).microseconds
        if value > 0:
            # value is % of current track: Calculate position in seconds
            new_pos =  (value * self.length()) / 100
            self._seek_position = int((new_pos - self.position()) * 1000000)
            self.last_position_change = now
        else:
            # callback from timer
            self._timer_running = False
        if time > 500000:
            self._dbus_proxy.mpris2_set_position(self.name() , self._seek_position)
            #self.set_position(self._seek_position / 1000000)
            self.last_position_change = now
        else:
            if not self._timer_running:
                self._timer_running = True
                self.trigger_timer_callback(500, self.schedule_set_mpris2_position)

