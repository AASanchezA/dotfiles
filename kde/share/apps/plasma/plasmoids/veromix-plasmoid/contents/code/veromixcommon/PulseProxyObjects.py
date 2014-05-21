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

import gettext
i18n = gettext.gettext

from .LADSPAEffects import *

try:
    import html
except:
    class html:
        @staticmethod
        def escape(arg):
            return arg

try:
    import urllib.parse
    unquote = urllib.parse.unquote
except:
    import urllib
    unquote = urllib.unquote

## FIXME bad name: how is one "channel" of a strereo stream called?
class SinkChannel():

    def __init__(self, name, volume):
        self.name = name
        self.volume = volume

    def get_name(self) :
        return self.name

    def get_volume(self):
        return self.volume

    def printDebug(self):
        print("    <SinkChannel>")
        print("      <name>" + self.name + "</name>")
        print("       <volume>" + self.volume + "</volume>")
        print("    </SinkChannel>")

class AbstractSink():
    # FIXME KDE
    DEFAULT_ICON = "audio-x-generic-symbolic"

    def __init__(self, pulseaudio, index, name, muted, volume, props):
        self.pulse_proxy = pulseaudio
        self.index =  index
        self.name =   name
        self.mute  =   muted
        self. volume  =   volume
        self.props = props
        self._update_nice_values(pulseaudio.veromix)

    def is_default(self):
        return False

    def get_index(self):
        return int(self.index)

    def get_name(self) :
        return self.name

    def toggle_mute(self):
        pass

    def step_volume_by(self, STEP, up):
        vol = self.get_volume()
        if up:
            vol = vol + STEP
        else:
            vol = vol - STEP
        if vol < 0:
            vol = 0
        if vol > 100: # FIXME self.get_max_volume_value():
            vol = 100 #self.get_max_volume_value()
        self.set_volume(self.volumeDiffFor(vol))

    def set_volume(self, values):
        pass

    def get_volume(self):
        val =0
        for t in list(self.volume.keys()):
            val += list(self.volume[t].values())[0]
        return int(val/ len(list(self.volume.keys())))

    def getChannels(self):
        channels = []
        for key in list(self.volume.keys()):
            t = self.volume[key]
            name = list(t.keys())[0]
            vol = list(t.values())[0]
            channels.append(SinkChannel(name,vol))
        return channels

    def volumeDiffFor(self, value):
        vol = []
        diff = self.get_volume() - value
        for key in list(self.volume.keys()):
            value = list(self.volume[key].values())[0] - diff
            if value < 0:
                value = 0
            vol.append(value )
        return vol

    def printDebug(self):
        print("<sink type=" +str(type(self))+ ">")
        print("  <index>" + self.index + "</index>")
        print("  <name>" + self.name + "</name>")
        print("  <mute>" + self.mute +  "</mute>")
        print("  <volume>")
        for channel in self.getChannels():
            channel.printDebug()
        print("  </volume>")
        print("  <properties>")
        for key in list(self.props.keys()):
            print("    <" + key + ">", self.props[key],"</" + key + ">")
        print("  </properties>")
        print("</sink>")

    def isMuted(self):
        # FIXME
        return self.is_muted()

    def is_muted(self):
        return self.mute == 1

    def get_monitor_name(self):
        return "Veromix monitor"

    ## testing

    def is_sourceoutput(self):
        return False

    def is_sinkoutput(self):
        return False

    def is_source(self):
        return self.is_sinkoutput()

    def is_sinkinput(self):
        return False

    def is_sink(self):
        return False

    def is_media_player(self):
        return False

    def properties(self):
        return self.props

    def _update_nice_values(self, veromix=None):
        self._nice_text =  ""
        self._nice_title = self.name
        self._nice_icon = self.DEFAULT_ICON

    def get_nice_text(self):
        return html.escape(self._nice_text)

    def get_nice_title(self):
        return html.escape(self._nice_title)

    def get_nice_icon(self):
        return self._nice_icon

    def get_nice_title_and_name(self):
        return "<b>" + self.get_nice_title() + "</b> " + self.get_nice_text()

    def is_default_sink(self):
        return False

    def get_output_index(self):
        return int(self.get_index())

    def get_owner_module(self):
         if "owner_module" in self.props:
            return self.props["owner_module"]
         return None

    def has_monitor(self):
        if "has_monitor" in self.props:
            return (self.props["has_monitor"] == "True")
        return False

class SinkInfo(AbstractSink):
    # FIXME KDE
    DEFAULT_ICON = "audio-card-symbolic"

    def __init__(self, pulseaudio, index, name, muted, volume, props, ports, active_port):
        AbstractSink.__init__(self, pulseaudio, index, name, muted, volume, props)
        self.ports=ports
        self.active_port=active_port

    def is_sink(self):
        return True

    def be_default_sink(self):
        self.pulse_proxy.set_default_sink(self.name)

    def is_default(self):
        if "isdefault" in self.props:
            return self.props["isdefault"] == "True"
        return False

    def set_volume(self, values):
        self.pulse_proxy.set_sink_volume(self.index, values)

    def toggle_mute(self):
        if self.isMuted():
            self.pulse_proxy.set_sink_mute(self.index, False)
        else:
            self.pulse_proxy.set_sink_mute(self.index, True)

    def set_port(self, portstr):
         self.pulse_proxy.set_sink_port(self.index,portstr)

    def toggle_monitor(self):
        self.pulse_proxy.toggle_monitor_of_sink(self.index, self.get_monitor_name())

    def kill(self):
        if self.is_ladspa_sink():
            self.remove_ladspa_sink()

    def set_ladspa_sink(self,parameters):
        self.pulse_proxy.set_ladspa_sink(int(self.index), int(self.props["owner_module"]), str(parameters))

    def remove_ladspa_sink(self):
        self.pulse_proxy.remove_ladspa_sink(int(self.props["owner_module"]))

    def remove_combined_sink(self):
        self.pulse_proxy.remove_combined_sink(int(self.props["owner_module"]))

    def is_default_sink(self):
        if "isdefault" in self.props:
            return self.props["isdefault"] == "True"
        return False

    def _update_nice_values(self, veromix=None):
        self._nice_text =  ""
        self._nice_title = self.name
        self._nice_icon = self.DEFAULT_ICON
        text = ""
        try:
            self._nice_title = self.props["device_name"]
        except:
            pass

    def move_sink_input(self, target_sink):
        self.pulse_proxy.move_sink_input(int(target_sink), int(self.get_index()))

    def is_ladspa_sink(self):
        return "device.ladspa.module" in self.props.keys()

    def get_ladspa_master(self):
        return self.get_name()

class SinkInputInfo(AbstractSink):

    def is_sinkinput(self):
        return True

    def set_volume(self, values):
        self.pulse_proxy.set_sink_input_volume(self.index, values)

    def toggle_mute(self):
        if self.isMuted():
            self.pulse_proxy.set_sink_input_mute(self.index, False)
        else:
            self.pulse_proxy.set_sink_input_mute(self.index, True)

    def toggle_monitor(self):
        self.pulse_proxy.toggle_monitor_of_sinkinput(self.index, self.get_output_index(), self.get_monitor_name())

    def kill(self):
        self.pulse_proxy.sink_input_kill(self.index)

    def _update_nice_values(self, veromix=None):
        text =  self.name
        bold = self.props["app"]
        iconname = None

        if self.props["app_icon"] != "None":
            iconname = self.props["app_icon"]
        if veromix:
            if iconname == None and  self.props["app"] != "None":
                iconname = veromix.query_application(self.props["app"], self.DEFAULT_ICON)
        if bold == "knotify":
            bold = i18n("Event Sounds")
            text = ""
            iconname = 'dialog-information'
        if bold == "npviewer.bin" or bold == "plugin-container":
            bold = i18n("Flash Player")
            text = ""
            iconname = 'flash'
        if bold == "chromium-browser":
            bold = i18n("Chromium Browser")
            text = ""
        if bold == "Skype":
            if text == "Event Sound":
                text = i18n("Event Sound")
            if text == "Output":
                text = i18n("Voice Output")

        if veromix:
            if text == "LADSPA Stream" or ("media.name" in self.props.keys() and self.props["media.name"] == "LADSPA Stream"):
                for sink in veromix.get_sink_widgets():
                    if sink.pa_sink_proxy().get_owner_module() == self.get_owner_module():
                        bold = sink.pa_sink_proxy().props["device.ladspa.name"]
                        text = ""
                        iconname = sink.pa_sink_proxy().props["device.icon_name"]

        # FIXME
        if bold in ["", "None", None]:
            bold = text
            text = ""

        if text in ["None", None]:
            text = ""

        if iconname in ["", "None", None]:
            iconname = self.DEFAULT_ICON # FIXME "mixer-pcm"
        self._nice_text = text
        self._nice_title = bold
        self._nice_icon = iconname

    def get_output_index(self):
        return int(self.props["sink"])

class SourceInfo(AbstractSink):
    DEFAULT_ICON = "audio-input-microphone-symbolic"

    def __init__(self, pulseaudio, index, name, muted, volume, props, ports, active_port):
        AbstractSink.__init__(self, pulseaudio, index, name, muted, volume, props)
        self.ports=ports
        self.active_port=active_port

    def is_sinkoutput(self):
        return True

    def set_volume(self, values):
        self.pulse_proxy.set_source_volume(self.index, values)

    def toggle_mute(self):
        if self.isMuted():
            self.pulse_proxy.set_source_mute(self.index, False)
        else:
            self.pulse_proxy.set_source_mute(self.index, True)

    def set_port(self, portstr):
         self.pulse_proxy.set_source_port(self.index,portstr)

    def toggle_monitor(self):
        self.pulse_proxy.toggle_monitor_of_source(self.index, self.get_monitor_name())

    def kill(self):
        pass

    def _update_nice_values(self, veromix=None):
        self._nice_text =  ""
        self._nice_title = self.name
        self._nice_icon = self.DEFAULT_ICON
        if "description" in self.props.keys():
            self._nice_title = self.props["description"]
#            self._nice_text = self.name

class SourceOutputInfo(AbstractSink):

    def is_sourceoutput(self):
        return True

    def set_volume(self, values):
        pass

    def toggle_mute(self):
        pass

    def kill(self):
        pass

    def toggle_monitor(self, parent):
        pass

    def get_volume(self):
        return 0

    def getChannels(self):
        return []

    def _update_nice_values(self, veromix=None):
        self._nice_text =  ""
        self._nice_title = self.name
        self._nice_icon = self.DEFAULT_ICON
        if "description" in self.props.keys():
            self._nice_title = self.props["description"]
            self._nice_text = self.name

        if self.name.find("ALSA") == 0 and "application.process.binary" in self.props.keys():
            self._nice_title = self.props[ "application.process.binary"]
            self._nice_text =  self.props[ "application.name"]

        if "application.icon_name" in self.props.keys():
            self._nice_icon = self.props["application.icon_name"]

        if veromix:
            if self._nice_icon == self.DEFAULT_ICON and  "app" in self.props.keys():
                self._nice_icon = veromix.query_application(self.props["app"], self.DEFAULT_ICON)

        if self._nice_icon is None and self._nice_title == "plugin-container":
            self._nice_icon = 'flash'

class CardProfile:
    def __init__(self, name, properties):
        self.name = name
        self.properties = properties
        self.description = properties["description"]
        # FIXME other values

    def printDebug(self):
        print("<CardProfile>")
        print("  <name>", self.name, "</name>")
        print("  <properties>")
        for key in list(self.properties.keys()):
            print("    <" + key + ">", self.properties[key],"</" + key + ">")
        print("  </properties>")
        print("</CardProfile>")

class CardInfo:
    def __init__(self, index, name, properties, active_profile_name, profiles_dict):
         self.index = index
         self.name = name
         self.properties = properties
         self.active_profile_name = active_profile_name
         self.profiles_dict = profiles_dict
         self.profiles = []
         for key in list(self.profiles_dict.keys()):
             self.profiles.append(CardProfile(key, self.profiles_dict[key] ))

    def get_property(self,key):
        if self.properties == None:
            return ""
        if key in list(self.properties.keys()):
            return self.properties[key]
        return ""

    def get_description(self):
        return self.get_property("device.description")

    def get_profiles(self):
        return self.profiles

    def get_active_profile(self):
        for profile in self.card_profiles():
            if self.active_profile_name == profile.name:
                return profile
        return None

    def get_active_profile_name(self):
        return self.active_profile_name

    def printDebug(self):
        print("<CardInfo>")
        print("  <index>", self.index,  "</index>")
        print("  <name>", self.name, "</name>")
        print("  <properties>")
        for key in list(self.properties.keys()):
            print("    <" + key + ">", self.properties[key],"</" + key + ">")
        print("  </properties>")
        print("</CardInfo>")

class ModuleInfo:

    def __init__(self, index, name, argument, n_used, auto_unload):
        self.index = int(index)
        self.name = name
        self.argument = argument
        self.n_used = n_used
        self.auto_unload = auto_unload

    def get_index(self):
        return self.index

    def set_pa_sink_proxy(self, pa_sink_proxy):
        self.pa_sink_proxy = pa_sink_proxy
        self.ladspa_parse_module_info(self.argument, self.pa_sink_proxy)

    def get_ladspa_nice_title(self):
        text = ""
        try:
            if self.is_ladspa_preset():
                text = str(self.get_ladspa_name()) + " - " + str(self.get_ladspa_preset_name())
            else:
                text = str(self.get_ladspa_name())
        except:
            pass
        return text

    def ladspa_parse_module_info(self, string, pa_sink_proxy):
        args = {}
        controls = string.split(" ")
        for entry in controls:
            s = entry.split("=")
            if len(s) == 2:
                args[s[0]]=s[1]
        args["name"] = ""
        if "device.ladspa.name" in pa_sink_proxy.props.keys():
            args["name"] = pa_sink_proxy.props["device.ladspa.name"]
        args["preset_name"] = unquote(str(args["sink_name"]))
        self.ladspa_module_info = args

    def get_ladspa_effect_name(self):
        return self.get_ladspa_label()

    def get_ladspa_preset_name(self):
        return self.ladspa_module_info["preset_name"]

    def get_ladspa_name(self):
        return self.ladspa_module_info["name"]

    def get_ladspa_label(self):
        return self.ladspa_module_info["label"]

    def get_ladspa_control_string(self):
        return self.ladspa_module_info["control"]

    def get_ladspa_control(self):
        string = self.get_ladspa_control_string()
        controls = []
        if str(string) != "":
            controls = string.split(",")
        return controls

    def get_lasapa_number_of_controls(self):
        return len(self.get_ladspa_control())

    def get_ladspa_effect_settings(self):
        effect = None
        for preset in LADSPAEffects().effects():
            if preset["label"] == self.get_ladspa_label():
                effect = preset
        return effect

    def is_ladspa_preset(self):
        return self.get_ladspa_name() != self.get_ladspa_preset_name()

    def get_ladspa_scale(self, number):
        effect = self.get_ladspa_effect_settings()
        return effect["scale"][number]

    def get_ladspa_range(self, number):
        effect = self.get_ladspa_effect_settings()
        return effect["range"][number]

    def get_ladspa_scaled_range(self, number):
        scale = self.get_ladspa_scale(number)
        scaled = [0,0]
        scaled[0] = (self.get_ladspa_range(number)[0]) * scale
        scaled[1] = (self.get_ladspa_range(number)[1]) * scale
        return scaled

    def get_ladspa_effect_label(self, number):
        effect = self.get_ladspa_effect_settings()
        return effect["labels"][number]

    def get_ladspa_control_value(self, number):
        return float(self.get_ladspa_control()[number])

    def get_ladspa_control_value_scaled(self, number):
        return int(self.get_ladspa_scale(number) * self.get_ladspa_control_value(number))

    def set_ladspa_sink(self, values, pa_sink_proxy):
        control = ""
        effect = self.get_ladspa_effect_settings()
        i = 0

        # multiply (visible) values with scale
        for val in values:
            scale = self.get_ladspa_scale(i)
            control = control +  str(float(val)/float(scale)) + ","
            i = i + 1
        self.ladspa_module_info["control"] = control[:-1]
        parameters = "sink_name=%(sink_name)s master=%(master)s plugin=%(plugin)s  label=%(label)s control=%(control)s" % self.ladspa_module_info
        pa_sink_proxy.set_ladspa_sink(parameters)

    def get_ladspa_master(self):
        return self.ladspa_module_info["master"]

    def save_preset(self, name=None):
        if name != None:
            self.ladspa_module_info["preset_name"] = str(name)
            self.ladspa_module_info["sink_name"] = str(name)
        LADSPAPresetLoader().write_preset(self.ladspa_module_info)

