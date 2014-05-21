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

from PyQt4.QtGui import *
from SinkInputUI import InputSinkUI
from SinkInputUI import SinkUI
from SinkMbeqUI import SinkMbeqUI

class SortedLayout(QGraphicsLinearLayout):

    def __init__(self, orient, reverse):
        QGraphicsLinearLayout.__init__(self, orient)
        self.reverse= reverse
        self.channels = {}
        self.sink_pool = []
        self.sink_input_pool = []

    def get_new_sink_input(self, veromix):
        if len(self.sink_input_pool) == 0:
            return InputSinkUI(veromix)
        else:
            val = self.sink_input_pool[0]
            self.sink_input_pool.remove(val)
            val.show()
            return val

    def get_new_sink(self, veromix, sink):
        sink_type = None
        if "device.ladspa.module" in sink.properties().keys(): # and
            sink_type = sink.properties()["device.ladspa.module"]         #"device.ladspa.module"
            return self._get_new_ladspa_sink(veromix, str(sink_type))
        else:
            return self._get_new_sink(veromix)

    def _get_new_ladspa_sink(self, veromix, sink_type):
        pool =  []
        for sink in self.sink_pool:
            # FIXME
            if sink.get_ladspa_type() == "ladspa":
                pool.append(sink)
        if len(pool) == 0:
            return SinkMbeqUI(veromix)
        else:
            val = pool[0]
            self.sink_pool.remove(val)
            val.show()
            return val

    def _get_new_sink(self, veromix):
        if len(self.sink_pool) == 0:
            return SinkUI(veromix)
        else:
            val = self.sink_pool[0]
            self.sink_pool.remove(val)
            val.show()
            return val

    def getChannels(self):
        return self.channels

    def get_source_widgets(self):
        return self._get_source_widgets(self.channels.values())

    def _get_source_widgets(self, objects):
        toreturn = []
        for obj in objects :
            if obj.isSourceOutput():
                toreturn.append(obj)
        return toreturn

    def get_sinkoutput_widgets(self):
        return self._get_sinkoutput_widgets(self.channels.values())

    def _get_sinkoutput_widgets(self, objects):
        toreturn = []
        for obj in objects :
            if obj.isSinkOutput():
                toreturn.append(obj)
        return toreturn

    def get_sink_widgets(self):
        return self._get_sink_widgets(self.channels.values())

    def _get_sink_widgets(self, objects):
        toreturn = []
        for obj in objects :
            if obj.isSink():
                toreturn.append(obj)
        return toreturn

    def get_sinkinput_widgets(self):
        return self._get_sinkinput_widgets(self.channels.values())

    def _get_sinkinput_widgets(self, objects):
        toreturn = []
        for obj in objects :
            if obj.isSinkInput():
                toreturn.append(obj)
        return toreturn

    def get_mediaplayer_widgets(self):
        toreturn = []
        for index in self.channels.keys() :
            if self.channels[index].isNowplaying():
                toreturn.append(self.channels[index])
        return self._get_mediaplayer_widgets(self.channels.values())

    def _get_mediaplayer_widgets(self, objects):
        toreturn = []
        for obj in objects :
            if obj.isNowplaying():
                toreturn.append(obj)
        return toreturn

    def getChannel(self, key):
        if key in self.channels.keys():
            return self.channels[key]
        return None

    def addChannel(self, key, widget):
        if(key not in self.channels.keys()):
            self.channels[key]  = widget
            sorting = self.sort(self.channels.values())
            index = sorting.index(widget)
            self.insertItem(index, widget )

    def removeChannel(self, key):
        if(key  in self.channels.keys()):
            self.channels[key].hide()
            self.removeItem(self.channels[key])
            if self.channels[key].isSinkInput():
                self.sink_input_pool.append(self.channels[key])
            if self.channels[key].isSink():
                self.sink_pool.append(self.channels[key])
            #self.channels[key].deleteLater()
            del self.channels[key]

    def check_ItemOrdering(self):
        while(self.needs_ordering()):
            self.order_items()

    def sorted_channels(self):
        return self.sort(self.channels.values())

    def order_items(self):
        sorting = self.sort(self.channels.values())
        for i in range(0,len(sorting)):
            if self.itemAt(i).graphicsItem ()  != sorting[i]:
                item = self.itemAt(i).graphicsItem()
                index = sorting.index(item)
                self.insertItem(index , item )
                return

    def needs_ordering(self):
        sorting = self.sort(self.channels.values())
        for i in range(0,len(sorting)):
            if self.itemAt(i).graphicsItem ()  != sorting[i]:
                return True
        return False

    def order_index(self, widget):
        return self.sort(self.channels.values()).index(widget)

    def sort(self,objects):
        sources = self._sort_by_attribute(self._get_source_widgets(objects), '_name')
        sourceoutputs = self._sort_by_attribute(self._get_sinkoutput_widgets(objects), '_name')
        sinks = self._sort_by_attribute(self._get_sink_widgets(objects), '_name')
        sink_inputs = self._sort_by_attribute(self._get_sinkinput_widgets(objects), '_name')
        mediaplayers = self._sort_by_attribute(self._get_mediaplayer_widgets(objects), '_name')
        sorting = []
        for s in sinks:
            if s.isDefaultSink():
                sinks.remove(s)
                sinks.insert(0,s)
        for s in sourceoutputs:
            sorting.append(s)
            for so in sources:
                if int(s.index) == int(so.get_assotiated_source()):
                    sorting.append(so)

        #sinks.reverse()
        for s in sinks:
            sorting.append(s)
            for i in sink_inputs:
                if int(s.index) == int(i.getOutputIndex()):
                    sorting.append(i)
                    for m in mediaplayers:
                        assoc = m.get_assotiated_sink_input()
                        if assoc != None and int(i.index) == assoc.index:
                            sorting.append(m)
        for i in set(objects).difference(set(sorting)):
            sorting.append(i)
        return sorting

    def _sort_by_attribute(self, objects,sortAttrib):
        nlist = map(lambda object, sortAttrib=sortAttrib: (getattr(object, sortAttrib),object), objects)
        nlist.sort(reverse=self.reverse)
        return map(lambda (key, object): object, nlist)
