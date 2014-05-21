# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Nik Lutz <nik.lutz@gmail.com>
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


import sys
import os
import ctypes
import random
import time

from .lib_pulseaudio import *
from .PulseSink      import PulseSinkInputInfo, PulseSinkInfo
from .PulseSource    import PulseSourceOutputInfo, PulseSourceInfo
from .PulseClient    import PulseClientCtypes
from .PulseCard      import CardInfo
from VeromixUtils import in_unicode

PA_VOLUME_CONVERSION_FACTOR = 655.36



# A null method that can be given to pulse methods
def null_cb(a=None, b=None, c=None, d=None):
    #print "NULL CB"
    return

class PulseAudio():
    def __init__(self):
        self.initialize_variables()

    def set_receiver(self, event_receiver):
        self.receiver = event_receiver

    def initialize_variables(self):
        self._context = None
        self.sinks = {}
        self.sink_inputs = {}
        self.sources = {}
        self.loaded_modules = {}
        self.monitor_sinks = {}
        self.monitor_sink_inputs = {}
        self.monitor_sources = {}
        self.sink_inputs_to_restore = []
        self.module_stream_restore_argument = ""
        self.default_source_name = ""
        self.default_sink_name = ""
        self._null_cb =  None
        self.pa_mainloop_api = None
        self.pa_mainloop = None
        self._context_notify_cb = None
        self._pa_context_subscribe_cb  = None
        self._pa_context_index_cb  = None
        self._pa_stream_request_cb = None
        self._pa_stream_notify_cb  = None
        self._pa_sink_info_cb  = None
        self._pa_sink_input_info_list_cb  = None
        self._pa_card_info_cb = None
        self._pa_source_info_cb  = None
        self._pa_source_output_info_cb  = None
        self._pa_client_info_list_cb  = None
        self._pa_module_info_cb = None
        self.IS_READY = False
        self._autostart_meters = False
        self._meter_rate = 10

    def start_pulsing(self):
        self.pa_mainloop = pa_threaded_mainloop_new()
        pa_threaded_mainloop_start(self.pa_mainloop)
        pa_threaded_mainloop_lock (self.pa_mainloop)
        self.pa_mainloop_api = pa_threaded_mainloop_get_api(self.pa_mainloop)
        veromix = "VeroMix"
        self._context = pa_context_new(self.pa_mainloop_api, as_p_char(veromix))
        self._context_notify_cb = pa_context_notify_cb_t(self.context_notify_cb)
        pa_context_set_state_callback(self._context, self._context_notify_cb, None)
        pa_context_connect(self._context, None, 0, None)
        ##
        pa_threaded_mainloop_unlock (self.pa_mainloop)

    def pa_exit(self):
        #try:
        ##pa_context_exit_daemon(self._context, self._context_notify_cb, 0)
        pa_threaded_mainloop_lock (self.pa_mainloop)
        #pa_context_set_state_callback(self._context, None, None)
        #pa_context_disconnect(self._context)
        pa_context_unref(self._context)
        pa_threaded_mainloop_unlock (self.pa_mainloop)

        #pa_threaded_mainloop_stop(self.pa_mainloop)
        pa_threaded_mainloop_free(self.pa_mainloop)
        #pa_threaded_mainloop_wait(self.pa_mainloop)
        self.initialize_variables()

    def set_autostart_meters(self, aboolean):
        self._autostart_meters = aboolean
        if aboolean:
            for source in list(self.sources.values()):
                self.pa_create_monitor_stream_for_source(source)
            for sink in list(self.sinks.values()):
                self.pa_create_monitor_stream_for_sink(sink.index, sink.name)
            for sinkinput in list(self.sink_inputs.values()):
                self.pa_create_monitor_stream_for_sink_input(sinkinput.index, sinkinput.sink)
        else:
            for source in list(self.sources.values()):
                self.pa_disconnect_monitor_of_source(source.index)
            for sink in list(self.sinks.values()):
                self.pa_disconnect_monitor_of_sink(sink.index)
            for sinkinput in list(self.sink_inputs.values()):
                self.pa_disconnect_monitor_of_sinkinput(sinkinput.index)

#############

    def pulse_toggle_monitor_of_sinkinput(self, sinkinput_index, sink_index, name):
        if float(sinkinput_index) in list(self.monitor_sink_inputs.keys()):
            self.pa_disconnect_monitor_of_sinkinput(sinkinput_index)
        else:
            self.pa_create_monitor_stream_for_sink_input(sinkinput_index, sink_index)

    def pa_disconnect_monitor_of_sinkinput(self, sinkinput_index):
        if float(sinkinput_index) in list(self.monitor_sink_inputs.keys()):
            pa_stream_disconnect(self.monitor_sink_inputs[float(sinkinput_index)])
            del self.monitor_sink_inputs[float(sinkinput_index)]

            sink = self.sink_inputs[int(sinkinput_index)]
            sink.set_has_monitor(False)
            self.receiver.sink_input_info(sink)

    def pa_create_monitor_stream_for_sink_input(self, index, sink_index, force = False):
        if not index in list(self.monitor_sink_inputs.keys()) or force :
            sink = self.sinks[float(sink_index)]

            ss = pa_sample_spec()
            ss.channels = 1
            ss.format = PA_SAMPLE_FLOAT32LE
            ss.rate = self._meter_rate
            #ss.rate = sink.sample_spec.rate

            pa_stream = pa_stream_new(self._context, as_p_char("Veromix sinkinput peak detect"), ss, None)
            pa_stream_set_monitor_stream(pa_stream, index)
            pa_stream_set_read_callback(pa_stream, self._pa_stream_request_cb, index)
            #pa_stream_set_suspended_callback(pa_stream, self._pa_stream_notify_cb, None)
            # FIXME We often get the wrong monitor_source here.
            pa_stream_connect_record(pa_stream, as_p_char(sink.monitor_source), None, PA_STREAM_PEAK_DETECT)
            self.monitor_sink_inputs[float(index)] =  pa_stream

            sinkinput = self.sink_inputs[int(index)]
            sinkinput.set_has_monitor(True)
            self.receiver.sink_input_info(sinkinput)


###########

    def pulse_toggle_monitor_of_sink(self, sink_index, name):
        if float(sink_index) in list(self.monitor_sinks.keys()):
            self.pa_disconnect_monitor_of_sink(sink_index)
        else:
            self.pa_create_monitor_stream_for_sink(sink_index, name)

    def pa_disconnect_monitor_of_sink(self, sink_index):
        if float(sink_index) in list(self.monitor_sinks.keys()):
            pa_stream_disconnect(self.monitor_sinks[float(sink_index)])
            del self.monitor_sinks[float(sink_index)]

            sink = self.sinks[float(sink_index)]
            sink.set_has_monitor(False)
            self.receiver.sink_info(sink)

    def pa_create_monitor_stream_for_sink(self, index, name, force = False):
        if not index in list(self.monitor_sinks.keys()) or force :
            if float(index) not in list(self.sinks.keys()):
                return
            sink = self.sinks[float(index)]
            samplespec = pa_sample_spec()
            samplespec.channels = 1
            samplespec.format = PA_SAMPLE_FLOAT32LE
            samplespec.rate = self._meter_rate
            #samplespec.rate = sink.sample_spec.rate

            pa_stream = pa_stream_new(self._context, as_p_char("Veromix sink peak detect"), samplespec, None)
            pa_stream_set_read_callback(pa_stream, self._pa_sink_stream_request_cb, index+1)
            #pa_stream_set_suspended_callback(pa_stream, self._pa_stream_notify_cb, None)

            pa_stream_connect_record(pa_stream, as_p_char(sink.monitor_source), None, PA_STREAM_PEAK_DETECT)
            self.monitor_sinks[float(index)] =  pa_stream

            sink.set_has_monitor(True)
            self.receiver.sink_info(sink)


###########

    def pulse_toggle_monitor_of_source(self, source_index, name):
        if float(source_index) in list(self.monitor_sources.keys()):
            self.pa_disconnect_monitor_of_source(source_index)
        else:
            self.pa_create_monitor_for_source(source_index, self.sources[float(source_index)], name)

    def pa_disconnect_monitor_of_source(self, source_index):
        if float(source_index) in list(self.monitor_sources.keys()):
            pa_stream_disconnect(self.monitor_sources[float(source_index)])
            del self.monitor_sources[float(source_index)]

    def pa_create_monitor_stream_for_source(self, source):
        self.pa_create_monitor_for_source(source.index, source, source.name)

    def pa_create_monitor_for_source(self, index, source, name, force = False):
        if not index in self.monitor_sources or force :
            # Create new stream
            samplespec = pa_sample_spec()
            samplespec.channels = 1
            samplespec.format = PA_SAMPLE_FLOAT32LE
            samplespec.rate = self._meter_rate

            pa_stream = pa_stream_new(self._context, as_p_char("Veromix source peak detect"), samplespec, None)
            pa_stream_set_read_callback(pa_stream, self._pa_source_stream_request_cb, index)
            pa_stream_set_suspended_callback(pa_stream, self._pa_stream_notify_cb, None)

            device = pa_xstrdup(as_p_char(in_unicode(source.name)))
            pa_stream_connect_record(pa_stream, device, None, PA_STREAM_PEAK_DETECT)
            self.monitor_sources[float(index)] = pa_stream

            source.set_has_monitor(True)
            self.receiver.source_info(source)


############# callbacks
    def pa_context_index_cb(self, context, index, user_data):
        # Do nothing....
        return

    def pa_context_success_cb(self, context, c_int, user_data):
        return

    # pulseaudio connection status
    def context_notify_cb(self, context, userdata):
        try:
            ctc = pa_context_get_state(context)
            if ctc == PA_CONTEXT_READY:
                print("Pulseaudio connection ready...")
                self._null_cb = pa_context_success_cb_t(null_cb)
                self._pa_context_success_cb = pa_context_success_cb_t(self.pa_context_success_cb)
                self._pa_stream_request_cb = pa_stream_request_cb_t(self.pa_stream_request_cb)
                self._pa_source_stream_request_cb = pa_stream_request_cb_t(self.pa_source_stream_request_cb)
                self._pa_sink_stream_request_cb = pa_stream_request_cb_t(self.pa_sink_stream_request_cb)

                self._pa_stream_notify_cb = pa_stream_notify_cb_t(self.pa_stream_request_cb)
                self._pa_sink_info_cb = pa_sink_info_cb_t(self.pa_sink_info_cb)
                self._pa_context_subscribe_cb = pa_context_subscribe_cb_t(self.pa_context_subscribe_cb)
                self._pa_source_info_cb = pa_source_info_cb_t(self.pa_source_info_cb)
                self._pa_source_output_info_cb = pa_source_output_info_cb_t(self.pa_source_output_info_cb)

                self._pa_card_info_cb = pa_card_info_cb_t(self.pa_card_info_cb)
                self._pa_server_info_cb = pa_server_info_cb_t(self.pa_server_info_cb)

                self._pa_sink_input_info_list_cb = pa_sink_input_info_cb_t(self.pa_sink_input_info_cb)
                self._pa_client_info_list_cb = pa_client_info_cb_t(self.pa_client_info_cb)
                self._pa_module_info_cb = pa_module_info_cb_t(self.pa_module_info_cb)
                self._pa_context_index_cb = pa_context_index_cb_t(self.pa_context_index_cb)

                self.requestInfo()

                pa_context_set_subscribe_callback(self._context, self._pa_context_subscribe_cb, None);
                o = pa_context_subscribe(self._context, (pa_subscription_mask_t)
                                               (PA_SUBSCRIPTION_MASK_SINK |
                                                PA_SUBSCRIPTION_MASK_SOURCE|
                                                PA_SUBSCRIPTION_MASK_SINK_INPUT|
                                                PA_SUBSCRIPTION_MASK_SOURCE_OUTPUT|
                                                PA_SUBSCRIPTION_MASK_CLIENT|
                                                PA_SUBSCRIPTION_MASK_SERVER|
                                                PA_SUBSCRIPTION_MASK_CARD |
                                                PA_SUBSCRIPTION_MASK_MODULE), self._null_cb, None)
                self.IS_READY = True
                #pa_operation_unref(o)

            if ctc == PA_CONTEXT_FAILED :
                self.__print("Connection failed")
                pa_threaded_mainloop_signal(self.pa_mainloop, 0)

            if ctc == PA_CONTEXT_TERMINATED:
                self.__print("Connection terminated")
                #pa_threaded_mainloop_signal(self.pa_mainloop, 0)
                print("leaving veromix..............")

        except Exception as text:
            self.__print("ERROR context_notify_cb %s" % text)

    def requestInfo(self):
        if  not self.IS_READY :
            # this method is also called when a new client starts  up that starts this service..
            return

        o = pa_context_get_client_info_list(self._context, self._pa_client_info_list_cb, None)
        pa_operation_unref(o)

        o = pa_context_get_server_info(self._context, self._pa_server_info_cb, None)
        pa_operation_unref(o)

        o = pa_context_get_sink_info_list(self._context, self._pa_sink_info_cb, None)
        pa_operation_unref(o)

        o = pa_context_get_sink_input_info_list(self._context, self._pa_sink_input_info_list_cb, True)
        pa_operation_unref(o)

        o = pa_context_get_source_info_list(self._context, self._pa_source_info_cb, True)
        pa_operation_unref(o)

        o = pa_context_get_source_output_info_list(self._context, self._pa_source_output_info_cb, None)
        pa_operation_unref(o)

        o = pa_context_get_card_info_list(self._context, self._pa_card_info_cb, None)
        pa_operation_unref(o)

        o = pa_context_get_module_info_list(self._context, self._pa_module_info_cb, None)
        pa_operation_unref(o)

    def pa_context_subscribe_cb(self, context, event_type, index, user_data):
        try:
            et = event_type & PA_SUBSCRIPTION_EVENT_FACILITY_MASK
            if et == PA_SUBSCRIPTION_EVENT_SERVER:
                o = pa_context_get_server_info(self._context, self._pa_server_info_cb, None)
                pa_operation_unref(o)
                o = pa_context_get_source_info_list(self._context, self._pa_source_info_cb, None)
                pa_operation_unref(o)
                o = pa_context_get_sink_info_list(self._context, self._pa_sink_info_cb, None)
                pa_operation_unref(o)

            if et == PA_SUBSCRIPTION_EVENT_CARD:
                if event_type & PA_SUBSCRIPTION_EVENT_TYPE_MASK == PA_SUBSCRIPTION_EVENT_REMOVE:
                    self.receiver.card_remove(int(index))
                else:
                    o = pa_context_get_card_info_list(self._context, self._pa_card_info_cb, None)
                    pa_operation_unref(o)

            if et == PA_SUBSCRIPTION_EVENT_CLIENT:
                if event_type & PA_SUBSCRIPTION_EVENT_TYPE_MASK == PA_SUBSCRIPTION_EVENT_REMOVE:
                    self.receiver.client_remove(int(index))
                else:
                    o = pa_context_get_client_info(self._context, index, self._pa_client_info_list_cb, None)
                    pa_operation_unref(o)

            if et == PA_SUBSCRIPTION_EVENT_SINK_INPUT:
                if event_type & PA_SUBSCRIPTION_EVENT_TYPE_MASK == PA_SUBSCRIPTION_EVENT_REMOVE:
                    self.receiver.sink_input_remove(int(index))
                    if float(index) in list(self.monitor_sink_inputs.keys()):
                        del self.monitor_sink_inputs[float(index)]
                    if int(index) in list(self.sink_inputs.keys()):
                        del self.sink_inputs[int(index)]
                else:
                    o = pa_context_get_sink_input_info(self._context, int(index), self._pa_sink_input_info_list_cb, True)
                    pa_operation_unref(o)

            if et == PA_SUBSCRIPTION_EVENT_SINK:
                if event_type & PA_SUBSCRIPTION_EVENT_TYPE_MASK == PA_SUBSCRIPTION_EVENT_REMOVE:
                    self.receiver.sink_remove(int(index))
                    if float(index) in list(self.monitor_sinks.keys()):
                        del self.monitor_sinks[float(index)]
                    if float(index) in list(self.sinks.keys()):
                        del self.sinks[float(index)]
                else:
                    ## TODO: check other event-types
                    o = pa_context_get_sink_info_list(self._context, self._pa_sink_info_cb, None)
                    #o = pa_context_get_sink_info_list(self._context, self._pa_source_info_cb, None)
                    pa_operation_unref(o)

            if et == PA_SUBSCRIPTION_EVENT_SOURCE:
                if event_type & PA_SUBSCRIPTION_EVENT_TYPE_MASK == PA_SUBSCRIPTION_EVENT_REMOVE:
                    self.receiver.source_remove(int(index))
                    if float(index) in list(self.monitor_sources.keys()):
                        del self.monitor_sources[float(index)]
                else:
                    #o = pa_context_get_source_info_by_index(self._context, int(index), self._pa_source_info_cb, None)
                    o = pa_context_get_source_info_list(self._context, self._pa_source_info_cb, None)
                    pa_operation_unref(o)

            if et == PA_SUBSCRIPTION_EVENT_SOURCE_OUTPUT:
                if event_type & PA_SUBSCRIPTION_EVENT_TYPE_MASK == PA_SUBSCRIPTION_EVENT_REMOVE:
                    self.receiver.source_output_remove(int(index))
                else:
                    o = pa_context_get_source_output_info_list(self._context, self._pa_source_output_info_cb, None)
                    #o = pa_context_get_source_info_by_index(self._context,int(index), self._pa_source_output_info_cb, None)
                    pa_operation_unref(o)

            if et == PA_SUBSCRIPTION_EVENT_MODULE:
                if event_type & PA_SUBSCRIPTION_EVENT_TYPE_MASK == PA_SUBSCRIPTION_EVENT_REMOVE:
                    if int(index) in list(self.loaded_modules.keys()):
                        del self.loaded_modules[int(index)]
                else:
                    o = pa_context_get_module_info(self._context, int(index), self._pa_module_info_cb, None)
                    pa_operation_unref(o)
                    #o = pa_context_get_module_info_list(self._context, self._pa_module_info_cb, False)
                    #pa_operation_unref(o)

        except Exception as text:
            self.__print("pa :: ERROR pa_context_subscribe_cb %s" % text)

    def pa_server_info_cb(self, context, struct, user_data):
        self.default_source_name = struct[0].default_source_name
        self.default_sink_name = struct[0].default_sink_name
        #self.requestInfo()

    def pa_sink_input_info_cb(self, context, struct, index, user_data):
        if struct :
            sink = PulseSinkInputInfo(struct[0])
            #print ( pa_proplist_to_string(struct.contents.proplist))
            sink.set_has_monitor(float(sink.index) in list(self.monitor_sink_inputs.keys()))
            self.sink_inputs[int(sink.index)] = sink
            self.receiver.sink_input_info(sink)
            if self._autostart_meters:
                self.pa_create_monitor_stream_for_sink_input(sink.index, sink.sink)

    def pa_sink_info_cb(self, context, struct, index, data):
        if struct:
            sink = PulseSinkInfo(struct[0])
            sink.set_has_monitor((float(sink.index) in list(self.monitor_sinks.keys())))
            sink.updateDefaultSink(self.default_sink_name)
            self.sinks[float(sink.index)] = sink
            self.receiver.sink_info(sink)
            if self._autostart_meters:
                self.pa_create_monitor_stream_for_sink(sink.index, sink.name)

    def pa_client_info_cb(self, context, struct, c_int, user_data):
        return

    def pa_source_output_info_cb(self, context, struct, cindex, user_data):
        if struct:
            source = PulseSourceOutputInfo(struct[0])
            self.receiver.source_output_info(source)

    def pa_source_info_cb(self, context, struct, eol, user_data):
        if struct:
            source = PulseSourceInfo(struct[0])
            source.set_has_monitor((float(source.index) in list(self.monitor_sources.keys())))
            source.updateDefaultSource(self.default_source_name)
            self.sources[ float(struct.contents.index) ] = source
            self.receiver.source_info(source)
            if self._autostart_meters:
                self.pa_create_monitor_stream_for_source(source)

    def pa_card_info_cb(self, context, struct, cindex, user_data):
        if struct:
            info = CardInfo(struct[0])
            self.receiver.card_info(info)
            #print ( pa_proplist_to_string(struct.contents.proplist))

    def pa_stream_request_cb(self, stream, length, index):
      # This isnt quite right... maybe not a float.. ?
        #null_ptr = ctypes.c_void_p()
        data = POINTER(c_float)()
        pa_stream_peek(stream, data, ctypes.c_ulong(length))
        v = data[int(length / 4) - 1] * 100
        if (v < 0):
            v = 0
        if (v > 100):
            v = 99
        pa_stream_drop(stream)
        if index:
            self.receiver.volume_meter_sink_input(int(index), float(v))
            #print "volume_meter_sink_input(int, float)",index, v

    def pa_source_stream_request_cb(self, stream, length, index):
        # This isnt quite right... maybe not a float.. ?
        #null_ptr = ctypes.c_void_p()
        data = POINTER(c_float)()
        pa_stream_peek(stream, data, ctypes.c_ulong(length))
        v = data[int(length / 4) - 1] * 100
        if (v < 0):
            v = 0
        if (v > 100):
            v = 99
        pa_stream_drop(stream)
        if index:
            self.receiver.volume_meter_source(int(index), float(v))

    def pa_sink_stream_request_cb(self, stream, length, index_incr):
        index = index_incr - 1
        data = POINTER(c_float)()
        pa_stream_peek(stream, data, ctypes.c_ulong(length))
        v = data[int(length / 4) - 1] * 100
        if (v < 0):
            v = 0
        if (v > 100):
            v=99
        pa_stream_drop(stream)
        #print "volume_meter_sink(int, float)", v
        self.receiver.volume_meter_sink(int(index), float(v))

    def pa_module_info_cb(self, context, pa_module_info, index, user_data):
#        print ("pa_module_info", pa_module_info, index)
        if pa_module_info:
            self.loaded_modules[int(pa_module_info.contents.index)] = in_unicode(pa_module_info.contents.name)

            if in_unicode(pa_module_info.contents.name) == "module-ladspa-sink":
                self.receiver.module_info(int(pa_module_info.contents.index), in_unicode(pa_module_info.contents.name), in_unicode(pa_module_info.contents.argument), in_unicode(pa_module_info.contents.n_used), in_unicode(pa_module_info.contents.auto_unload))

                # Restore ladspa-effects
                moved = []
                for values in self.sink_inputs_to_restore:
                    sink_input = values[0]
                    parameters = values[1]
                    if str(pa_module_info.contents.argument) == parameters:
                        for sink in list(self.sinks.values()):
                            if sink.owner_module == int(pa_module_info.contents.index):
                                self.pulse_move_sink_input(sink_input.index, int(sink.index))
                                moved.append(values)
                for m in moved:
                    self.sink_inputs_to_restore.remove(values)
        return

################### misc

    #def pa_ext_stream_restore_delete( self, stream):
        ## Only execute this if module restore is loaded
        #if "module-stream-restore" in self.loaded_modules:
            #pa_ext_stream_restore_delete(self._context, stream, self._pa_context_success_cb, None)

####### unused

    def load_module_stream_restore(self):
        print("Reloading module-stream-restore ")
        pa_context_load_module(self._context, "module-stream-restore", self.module_stream_restore_argument, self._pa_context_index_cb, None)

    # Move a playing stream to a differnt output sink
    def move_sink(self, sink_index, output_name):
        self.__print("move_sink")
        pa_context_move_sink_input_by_name(self._context, sink_index, as_p_char(output_name), self._pa_context_success_cb, None)

################## card profile

    def pulse_set_card_profile(self, index, value):
#        operation = pa_context_set_card_profile_by_name(self._context,as_p_char(index),as_p_char(value), self._null_cb,None)
        operation = pa_context_set_card_profile_by_index(self._context,int(index),as_p_char(value), self._null_cb,None)
        pa_operation_unref(operation)
        return

################## volume
    def pulse_mute_stream(self, index):
        self.pulse_sink_input_mute(index, 1)
        return

    def pulse_unmute_stream(self, index):
        self.pulse_sink_input_mute(index, 0)
        return

    def pulse_mute_sink(self, index):
        self.pulse_sink_mute(index, 1)
        return

    def pulse_unmute_sink(self, index):
        self.pulse_sink_mute(index, 0)
        return

    def pulse_sink_input_kill(self, index):
        operation = pa_context_kill_sink_input(self._context,index, self._null_cb,None)
        pa_operation_unref(operation)
        return

    def pulse_sink_input_mute(self, index, mute):
        operation = pa_context_set_sink_input_mute(self._context,index,mute, self._null_cb,None)
        pa_operation_unref(operation)
        return

    def pulse_sink_mute(self, index, mute):
        "Mute sink by index"
        operation = pa_context_set_sink_mute_by_index(self._context, index,c_int(mute),self._null_cb,None)
        pa_operation_unref(operation)
        return

    def pulse_set_sink_port(self,index,portstr):
        "Switch ports by index and port string"
        operation = pa_context_set_sink_port_by_index(self._context,index, as_p_char(portstr),self._null_cb,None)
        pa_operation_unref(operation)
        return

    def pulse_set_default_sink(self, index):
        operation = pa_context_set_default_sink(self._context, as_p_char(str(index)),self._null_cb,None)
        pa_operation_unref(operation)
        return

    def pulse_source_mute(self, index, mute):
        "Mute sink by index"
        operation = pa_context_set_source_mute_by_index(self._context, index,mute,self._null_cb,None)
        pa_operation_unref(operation)
        return

    def pulse_set_source_port(self,index,portstr):
        "Switch ports by index and port string"
        operation = pa_context_set_source_port_by_index(self._context,index,portstr,self._null_cb,None)
        pa_operation_unref(operation)
        return

    def pulse_set_default_source(self, index):
        operation = pa_context_set_default_source(self._context, as_p_char(index),self._null_cb,None)
        pa_operation_unref(operation)
        return

    def pulse_set_sink_volume(self, index, vol):
        operation = pa_context_set_sink_volume_by_index(self._context,index,vol.toCtypes(), self._null_cb,None)
        pa_operation_unref(operation)
        return

    def pulse_set_source_volume(self, index, vol):
        operation = pa_context_set_source_volume_by_index(self._context, index, vol.toCtypes(), self._null_cb,None)
        pa_operation_unref(operation)
        return

    def pulse_set_sink_input_volume(self, index, vol):
        operation = pa_context_set_sink_input_volume(self._context,index,vol.toCtypes(),self._null_cb,None)
        pa_operation_unref(operation)
        return

    def pulse_move_sink_input(self, index, target):
        operation = pa_context_move_sink_input_by_index(self._context,index, target, self._null_cb, None)
        pa_operation_unref(operation)
        self.pa_create_monitor_stream_for_sink_input(index, target, True)
        return

    def pulse_move_source_output(self, index, target):
        operation = pa_context_move_source_output_by_index(self._context,index, target, self._null_cb, None)
        pa_operation_unref(operation)
        #self.pa_create_monitor_stream_for_source(int(index), self.sink_inputs[float(target)], "", True)
        return

    def set_ladspa_sink(self, sink_index, module_index, parameters):
        try:
            if sink_index > -1 and int(module_index) in list(self.loaded_modules.keys()):
                # collect connected sink_inputs
                for sinkinput in list(self.sink_inputs.values()):
                    if float(sinkinput.sink) in list(self.sinks.keys()):
                        if self.sinks[float(sinkinput.sink)].owner_module == module_index:
                            self.sink_inputs_to_restore.append([sinkinput, parameters])
                self.remove_ladspa_sink(module_index)

            o = pa_context_load_module(self._context, as_p_char("module-ladspa-sink"),as_p_char(parameters), self._pa_context_index_cb, None)
            pa_operation_unref(o)

        except Exception as e :
            print(e)

    def remove_ladspa_sink(self, index):
        for key in list(self.loaded_modules.keys()):
            if self.loaded_modules[key] == "module-ladspa-sink" and int(key) == index:
                o = pa_context_unload_module(self._context, int(key), self._null_cb, None)
                pa_operation_unref(o)

    def create_combined_sink(self, first_sink_index, second_sink_index):
        parameters="slaves=" + str(first_sink_index) + "," + str(second_sink_index)
        o = pa_context_load_module(self._context, "module-combine-sink",parameters, self._pa_context_index_cb, None)
        pa_operation_unref(o)

    def remove_combined_sink(self, index):
        for key in list(self.loaded_modules.keys()):
            if self.loaded_modules[key] == "module-combine-sink" and int(key) == index:
                o = pa_context_unload_module(self._context, int(key), self._null_cb, None)
                pa_operation_unref(o)

    def __print(self, text):
        print(text)
        return

#if __name__ == '__main__':
    #c = PulseAudio()


    # Unload & reload stream-restore module with restore_device option disabled (to ensure that previously cached per-client sinks are not used)
    #for key in self.loaded_modules.keys():
        #if self.loaded_modules[key] == "module-stream-restore":
            #o = pa_context_unload_module(self._context, int(key), self._null_cb, None)
            #pa_operation_unref(o)
    #o = pa_context_load_module(self._context, "module-stream-restore", "restore_device=false", self._pa_context_index_cb, None)
    #pa_operation_unref(o)
    #print "sink_index", sink_index, self.sinks.keys()
