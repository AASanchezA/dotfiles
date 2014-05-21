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


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import *

from veromixcommon.MediaPlayer import *

class NowPlayingController(QObject, MediaPlayer):

    data_updated = pyqtSignal()

    def __init__(self, veromix, source):
        QObject.__init__(self)
        MediaPlayer.__init__(self)
        self.veromix = veromix
        self.proxy = source

    def init_connection(self):
        self.connect_nowplaying()

    def disconnect(self):
        pass

    def connect_nowplaying(self):
        self.veromix.applet.nowplaying_player_dataUpdated.connect(self.on_nowplaying_data_updated)

    def on_nowplaying_data_updated(self, name, values):
        if name == self.name():
            self.parse_values(values)

    def parse_values(self,data):
        state = self.state()
        changed = False
        if QString('State') in data:
            if data[QString('State')] == u'playing':
                self.set_state(MediaPlayer.Playing)
            else:
                self.set_state(MediaPlayer.Paused)
            if state != self.state():
                changed = True
        if QString('Position') in data:
            v = data[QString('Position')]
            if v != self.position():
                self.set_position(v)
                changed = True

        if QString('Length') in data:
            v = data[QString('Length')]
            if v != self.length():
                changed = True
                self.set_length(v)

        if QString('Artwork') in data:
            val = data[QString('Artwork')]
            if self.artwork() !=  val:
                self.set_artwork(val)
                if val == None:
                    self.last_playing_icon = KIcon(self.get_pauseIcon())
                else:
                    self.last_playing_icon = QIcon(QPixmap(self.artwork))
        if changed:
            self.data_updated.emit()

    def name(self):
        return self.proxy.destination()

    def play(self):
        self.proxy.startOperationCall(self.proxy.operationDescription('play'))

    def pause(self):
        self.proxy.startOperationCall(self.proxy.operationDescription('pause'))

    def next_track(self):
        self.proxy.startOperationCall(self.proxy.operationDescription('next'))

    def prev_track(self):
        self.proxy.startOperationCall(self.proxy.operationDescription('previous'))

    def seek(self, position):
        pos = int (position * self.length()/100)
        op = self.proxy.operationDescription('seek')
        op.writeEntry("seconds",pos)
        self.proxy.startOperationCall(op)

    def is_nowplaying_player(self):
        return True

