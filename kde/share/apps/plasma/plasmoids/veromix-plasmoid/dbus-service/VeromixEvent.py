# -*- coding: utf-8 -*-
# Copyright (C) 2012 Nik Lutz <nik.lutz@gmail.com>
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

class VeromixEvent():

    def __init__(self, target):
        self.target = target

    def sink_input_info(self, sink):
        self.target.on_sink_input_info(sink)

    def sink_input_remove(self, int_index):
        self.target.on_remove_sink_input(int_index)

    def volume_meter_sink_input(self, int_index, float_value):
        self.target.on_volume_meter_sink_input(int_index, float_value)


    def sink_info(self, sink):
        self.target.on_sink_info(sink)

    def sink_remove(self, int_index):
        self.target.on_remove_sink(int_index)

    def volume_meter_sink(self, int_index, float_value):
        self.target.on_volume_meter_sink(int_index, float_value)


    def source_output_info(self, source):
        self.target.on_source_output_info(source)

    def source_output_remove(self, int_index):
        self.target.on_remove_source_output(int_index)


    def source_info(self, source):
        self.target.on_source_info(source)

    def source_remove(self, int_index):
        self.target.on_remove_source(int_index)

    def volume_meter_source(self, int_index, float_value):
        self.target.on_volume_meter_source(int_index, float_value)


    def card_info(self, card):
        self.target.on_card_info(card)

    def card_remove(self, card_index):
        self.target.on_remove_card(card_index)


    def client_remove(self, int_index):
        # FIXME
        pass

    def module_info(self, int_index, name, argument, n_used_string, autounload_string):
        self.target.on_module_info(int_index, name, argument, n_used_string, autounload_string)

