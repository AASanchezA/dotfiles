# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012 Nik Lutz <nik.lutz@gmail.com>
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

from PyKDE4.plasma import Plasma
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import *
from veromixcommon.Utils import *


class MuteButton(Plasma.IconWidget):

    def __init__(self , parent):
        Plasma.IconWidget.__init__(self)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed,True) )
        self.BIGSIZE= 24
        self.setPreferredSize(QSizeF(self.BIGSIZE,self.BIGSIZE))
        self.setMaximumSize(QSizeF(self.BIGSIZE,self.BIGSIZE))
        self.setParent(parent)
        self.play_Icon =  "audio-volume-high"
        self.muted_Icon =  "audio-volume-muted"

    def mouseMoveEvent(self,event):
        self.parent().startDrag(event)

    def setAbsSize(self, value):
        self.BIGSIZE = value
        self.setPreferredSize(QSizeF(self.BIGSIZE,self.BIGSIZE))
        self.setMaximumSize(QSizeF(self.BIGSIZE,self.BIGSIZE))

    def setMuted(self, boolean):
        if boolean :
            self.setSvg("icons/audio", self.muted_Icon)
        else:
            self.setSvg("icons/audio", self.play_Icon)

    # compatibility with kde 4.4
    def setSvg(self, path, name):
        svg = Plasma.Svg()
        svg.setImagePath("icons/audio")
        if svg.isValid():
            Plasma.IconWidget.setSvg(self,path, name)
        else:
            self.setIcon(KIcon(name))

class InputMuteButton(MuteButton):

    def __init__(self , parent) :
        MuteButton.__init__(self,parent)
        self.setParent(parent)
        self.big_name =  "mixer-pcm"
        self.status_icon = KIcon(self.play_Icon)
        #self.status_icon.setSvg("icons/audio", self.play_Icon)

    def setMuted(self, boolean):
        if boolean :
            self.status_icon = self.muted_Icon
        else:
            self.status_icon =  self.play_Icon
        self.setIcon(self._draw_icon())

    def setBigIconName(self, name):
        if self.big_name != name:
            self.big_name = name
            self.setIcon(self._draw_icon())

    def _draw_icon(self ):
        if self.status_icon == self.muted_Icon:
            size =  self.BIGSIZE
            size2= 22
            #pos = self.size().height() - size2 + int(size2/4)
            pos = 8
            orig =  KIcon(self.big_name).pixmap(size2, size2)
            #over = KIcon(self.status_icon).pixmap(size2,size2)
            over = pixmapFromSVG(self.status_icon)

            #over =  KIcon(self.big_name).pixmap(size2,size2)
            #orig = self.status_icon.pixmap(28,28)

            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)

            p = QPainter(pixmap)
            #p.fillRect(QRect(0,0,size,size),QColor(0,100,1,250))
            p.drawPixmap(0,0,orig)
            p.end()

            copy = QPixmap(pixmap)
            paint_copy = QPainter(copy)
            paint_copy.fillRect(pixmap.rect(), QColor(1,1,1,10))
            paint_copy.end()
            pixmap.setAlphaChannel(copy)

            paint = QPainter(pixmap)
            #over = KIconLoader.loadIcon(loader, "audio-volume-muted", KIconLoader.NoGroup, size2, KIconLoader.DefaultState, "", "", True)
            paint.drawPixmap( pos  , pos, over)
            paint.end()
            return QIcon(pixmap)
        else:
            return KIcon(self.big_name)
