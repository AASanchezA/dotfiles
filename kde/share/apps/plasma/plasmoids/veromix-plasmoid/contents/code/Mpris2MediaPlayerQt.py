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

class Mpris2MediaPlayerQt(QObject, Mpris2MediaPlayer):
    
    data_updated = pyqtSignal()
    
    def __init__(self, name, dbus_proxy):
        QObject.__init__(self)
        Mpris2MediaPlayer.__init__(self, name, dbus_proxy)
    
    def signal_data_updated(self):
        self.data_updated.emit()
        
    def url_path_of(self, string):
        return QUrl(string).path()

    def trigger_timer_callback(self, timeout, function):
        QTimer.singleShot(timeout, function)

    def create_pixmap(self, val):
        return QPixmap(val)

        
