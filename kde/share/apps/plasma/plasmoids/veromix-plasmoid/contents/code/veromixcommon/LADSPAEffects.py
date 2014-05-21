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

import os,re,math,shutil

_presets = None

try:
    import commands
    getstatusoutput = commands.getstatusoutput
except:
    import subprocess
    getstatusoutput = subprocess.getstatusoutput


class LADSPAPresetLoader:
    configdir = os.getenv('HOME') + "/.pulse"
    user_preset_directory = configdir + "/presets"

    def install_ladspa_presets_if_needed(self):
        veromix_path = os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.realpath(__file__), os.path.pardir)), os.path.pardir)) + "/data/presets"
        if os.path.exists(self.user_preset_directory):
            return
        print("Veromix copying default presets to: " + self.user_preset_directory)
        try:
            shutil.copytree(veromix_path, self.user_preset_directory)
        except:
            print("Veromix exception while copying presets: ")

    def get_user_preset_directory(self):
        return self.user_preset_directory

    def read_preset(self, filename):
        f = open(filename, "r")
        rawdata=f.read().split('\n')
        f.close

        preset = {
            #"plugins" =  #"mbeq"
            "label" : str(rawdata[1]),
            # "name" : "Multiband EQ",
            "name" :   str(rawdata[2]),
            #unused
            "preamp" : str(rawdata[3]),
            #"plugin": "mbeq_1197",
            "plugin" : str(rawdata[0]),
            "preset_name" : str(rawdata[4]),

            # unused currently
            "inputs" : "50,100,156,220,311,440,622,880,1250,1750,2500,3500,5000,10000,20000"
        }

        #"control": "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0",
        num_ladspa_controls = int(rawdata[5])
        control = ""
        for x in range(0, num_ladspa_controls):
            control = control + str(rawdata[6 + x]) + ","

        preset["control"] = control[:-1]

        effect = None
        for settings in LADSPAEffects().effects():
            if (settings["label"] == preset["label"]):
                effect = settings

        if effect:
            preset["range"] = effect["range"]
            #"range" : [[-70, 30],[-70, 30],[-70, 30],[-70, 30],[-70, 30],[-70, 30],[-70, 30],[-70, 30],[-70, 30],[-70, 30],[-70, 30],[-70, 30],[-70, 30],[-70, 30],[-70, 30]],
            preset["scale"] = effect["scale"]
            #"scale" : [1,1,1, 1,1,1, 1,1,1, 1,1,1, 1,1,1],
            preset["labels"] = effect["labels"]
            #"labels" : ["50Hz","100Hz","156Hz","220Hz","311Hz","440Hz","622Hz","880Hz","1250Hz","1750Hz","2500Hz","3500Hz","5000Hz","10000Hz","20000Hz",]

            _range = []
            for x in range(0, num_ladspa_controls):
                _range.append([-30,30])
            preset["range"] = _range

        else:
            _range = []
            for x in range(0, num_ladspa_controls):
                _range.append([0,100])
            preset["range"] = _range

            scale = []
            for x in range(0, num_ladspa_controls):
                scale.append(1)
            preset["scale"] = scale

            labels = []
            for x in range(0, num_ladspa_controls):
                labels.append("raw_"+str(x))
            preset["labels"] = labels

        return preset

    def presets(self, do_reload=False):
        global _presets
        if _presets == None or do_reload:
            self.read_presets()
            _presets = sorted(_presets, key=lambda k: k['preset_name'])
        return _presets

    def read_presets(self):
        global _presets
        _presets = []
        for path in self.listdir_fullpath(self.user_preset_directory):
            _presets.append(self.read_preset(path))

    def listdir_fullpath(self, directory):
        if os.path.exists(directory):
            dir_list = os.listdir(directory)
            return [os.path.join(directory, x) for x in os.listdir(directory) if x.endswith('.preset')]
        return []

    def preset_exists(self, name):
        return os.path.exists(self.preset_full_path(name))

    def preset_full_path(self,name):
        tmp = ''.join(c for c in name if c not in ['\\', '/'])
        return self.get_user_preset_directory() + "/" + tmp + ".preset"

    def write_preset(self, plugin_settings):
        if not os.path.exists(self.get_user_preset_directory()):
            os.path.mkdir(self.get_user_preset_directory())

        f = open(self.preset_full_path(str(plugin_settings["preset_name"])), "w")
        rawdata = []
        rawdata.append(str(plugin_settings["plugin"]))
        rawdata.append(str(plugin_settings["label"]))
        rawdata.append(str(plugin_settings["name"]))
        rawdata.append(str(2)) # preamp
        rawdata.append(str(plugin_settings["preset_name"]))

        controls = plugin_settings["control"].split(",")
        num_ladspa_controls = len(controls)
        rawdata.append(str(num_ladspa_controls))
        for i in controls:
            rawdata.append(str(i))

        effect = None
        for settings in LADSPAEffects().effects():
            if (settings["label"] == plugin_settings["label"]):
                effect = settings

        for i in effect["labels"]:
            rawdata.append(str(i))

        for i in rawdata:
            f.write(str(i)+'\n')
        f.close()

        found = False
        self.presets(True)

_effects = None
class LADSPAEffects:
    blacklist_file = os.getenv('HOME') + "/.pulse/veromix-ladspa-blacklist.conf"

    def effects(self, do_reload=False):
        global _effects
        if _effects == None or do_reload:
            blacklist = self.blacklist()
            _effects = []
            for effect in self.all_effects():
                if effect["preset_name"] not in blacklist:
                    _effects.append(effect)
        return _effects

    def all_effects(self):
        _all_effects = fetch_plugins()
        _all_effects = sorted(_all_effects, key=lambda k: k['preset_name'])
        return _all_effects

    def blacklist(self):
        if not os.path.exists(self.blacklist_file):
            return []
        f = open(self.blacklist_file, "r")
        rawdata = f.read().split('\n')
        f.close
        return rawdata

    def write_blacklist(self, blacklist):
        f = open(self.blacklist_file, "w")
        rawdata = []
        for entry in blacklist:
            f.write(str(entry)+'\n')
        f.close()
        self.effects(True)

    def ladspa_sdk_available(self):
        status,output = getstatusoutput("listplugins")
        #status2, output = commands.getstatusoutput("analyseplugin")
        return status == 0

def fetch_plugins():
    status,output = getstatusoutput("listplugins")
    if status != 0:
        print("Veromix LADSPA: command 'listplugins' returend an error - is it installed? Check if ladspa-sdk is installed.")
        return hardcoded_plugins()
    plugins = []
    for line in  output.split("\n"):
        if re.match (".*:$", line):
            name = line[0:-1]
            filename =  os.path.basename(name)
            try:
                status,out = getstatusoutput("analyseplugin " + filename)
                if status != 0:
                    print("Veromix LADSPA: command 'analyseplugin' returend an error:")
                    print(out)
                else:
                    lines = out.split("\n")

                    "one file (for example amp.so can have multiple pluigin-definitions)"
                    plugin = []
                    for line in lines:
                        if len(line) == 0:
                            if len(plugin) > 1:
                                p = None
                                #print plugin
                                p = extract_plugin(filename, plugin)
                                if p:
                                    plugins.append(p)
                                plugin = []
                        else:
                            plugin.append(line)
            except:
                print("Problem during plugin extraction")

    if len(plugins) == 0:
        return hardcoded_plugins()
    return plugins

def extract_plugin(filename, lines):
    definition = {
        "label" : value_from_line(lines[1]),
        # FIXME
        "preset_name" : value_from_line(lines[0]) + " (" + filename[0:-3] + ")" ,
        "plugin" : filename[0:-3],
        "name" : value_from_line(lines[0])
        }
    has_input = False
    has_output = False

    port_hints = lines[10:]
    for port_hint in port_hints:
        # "50Hz gain (low shelving)" input, control, -70 to 30, default 0
        match = re.match(r'^.*\"(.*)\" input, control, (-?[\d\.]*) to (-?[\d\.]*), default (-?[\d\.]*)(, logarithmic)?', port_hint)
        if match:
            if "labels" not in list(definition.keys()):
                definition["labels"] = []
            definition["labels"].append(match.group(1))
            #print match.group(1), match.group(2), match.group(3)

            if "range" not in list(definition.keys()):
                definition["range"] = []
            lower = match.group(2)
            upper = match.group(3)
            if lower == "...":
                lower = "-1000"
            if upper == "...":
                upper = "1000"
            lower = float(lower) if '.' in lower else int(lower)
            upper = float(upper) if '.' in upper else int(upper)
            definition["range"].append([lower,upper])

            if "control" not in list(definition.keys()):
                definition["control"] = ""
                definition["controlnumbers"] = []
            definition["control"] = definition["control"] + "," + str(match.group(4))
            definition["controlnumbers"].append(float(match.group(4)) if '.' in match.group(4) else int(match.group(4)))

            if "control_type" not in list(definition.keys()):
                definition["control_type"] = []
            if match.group(5):
                definition["control_type"].append("log")
            else:
                definition["control_type"].append("dec")

        # "Input" input, audio
        match = re.match(r'.*" input, audio', port_hint)
        if match:
            has_input = True

        #"Output" output, audio
        match = re.match(r'.*" output, audio', port_hint)
        if match:
            has_output = True

        #"latency" output, control
        match = re.match(r'.*" output, control', port_hint)
        if match:
            pass


    # Currently this module only works with plugins that have one audio input port named "Input" and one output with name "Output".
    # http://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules#module-ladspa-sink
    if has_input and has_output:
            # some cleanup
        if "control" in list(definition.keys()):
            definition["control"] = definition["control"][1:]
            definition["scale"] = []
            index = 0
            for assoc in definition["range"]:
                lower = assoc[0]
                upper = assoc[1]
                control_default = definition["controlnumbers"][index]
                index = index + 1
                num = 1
                if isinstance(lower, float):
                    num = len(str(lower).split(".")[1])
                if isinstance(upper, float):
                    tmp = len(str(upper).split(".")[1])
                    if tmp > num:
                        num = tmp
                if isinstance(control_default, float):
                    tmp = len(str(control_default).split(".")[1])
                    if tmp > num:
                        num = tmp
                if (upper - lower) < 11:
                    definition["scale"].append(pow(10,num))
                else:
                    definition["scale"].append(1)
        else:
            definition["labels"] = []
            definition["range"] = []
            definition["control"] = ""
            definition["scale"] = []
        return definition
    return None

def value_from_line(line):
    match = re.search(r'"(.*)"', line)
    return match.group(0)[1:-1]

def hardcoded_plugins():
    return [
        {
            "preset_name" : "Multiband EQ",
            "label" : "mbeq",
            "name" : "Multiband EQ",
            "plugin": "mbeq_1197",
            "control": "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0",
            "range" : [[-70, 30],[-70, 30],[-70, 30],
                        [-70, 30],[-70, 30],[-70, 30],
                        [-70, 30],[-70, 30],[-70, 30],
                        [-70, 30],[-70, 30],[-70, 30],
                        [-70, 30],[-70, 30],[-70, 30]],
            "scale" : [1,1,1, 1,1,1, 1,1,1, 1,1,1, 1,1,1],
            "labels" : ["50Hz","100Hz","156Hz",
                        "220Hz","311Hz","440Hz",
                        "622Hz","880Hz","1250Hz",
                        "1750Hz","2500Hz","3500Hz",
                        "5000Hz","10000Hz","20000Hz",] },

        {
            "preset_name" : "DJ Equalizer",
            "label" : "dj_eq_mono",
            "name" : "DJ Equalizer",
            "plugin": "dj_eq_1901",
            "control": "0,0,0",
            "range" : [[-70, 6],[-70, 6],[-70, 6]],
            "scale" : [1,1,1],
            "labels" : ["Lo gain","Mid gain","Hi gain"]},

        {
            "preset_name" : "Flanger",
            "label" : "flanger",
            "name" : "Flanger",
            "plugin": "flanger_1191",
            "control": "6.325,2.5,0.33437,0",
            "range" : [[0.1, 25],[0, 10],[0, 100],[-1, 1]],
            "scale" : [100,10,10, 10],
            "labels" : ["Delay base","Max slowdown","LFO frequency", "Feedback"] },

        {
            "preset_name" : "Pitch Scaler",
            "label" : "pitchScale",
            "name" : "Pitch Scaler",
            "plugin": "pitch_scale_1193",
            "control": "1",
            "range" : [[0.5, 2]],
            "scale" : [100],
            "labels" : ["Co-efficient"]},

        {
            "preset_name" : "Multivoice Chorus",
            "label" : "multivoiceChorus",
            "name" : "Multivoice Chorus",
            "plugin": "multivoice_chorus_1201",
            "control": "1,10,0.5,1,9,0",
            "range" : [[1, 8], [10, 40], [0, 2], [0, 5], [2, 30], [-20, 0]],
            "scale" : [1,10,10,10, 10, 10 ],
            "labels" : ["Voices", "Delay base", "Voice separation", "Detune", "LFO frequency", "Output attenuation"] } ]

        ## GOOD
        #sink_name="sink_name=ladspa_output.dj_eq_1901.dj_eq."+str(self.ladspa_index)
        #plugin = "plugin=dj_eq_1901"
        #label = "label=dj_eq_mono"
        #control = "control=0,0,0"

        # fun!
        #sink_name="sink_name=ladspa_output.multivoice_chorus_1201.multivoiceChorus."+str(self.ladspa_index)
        #plugin = "plugin=multivoice_chorus_1201"
        #label = "label=multivoiceChorus"
        #control = "control=0,0,0,0,0,0"

        ## fun
        #sink_name="sink_name=ladspa_output.pitch_scale_1193.pitchScale."+str(self.ladspa_index)
        #plugin = "plugin=pitch_scale_1193"
        #label = "label=pitchScale"
        #control = "control=1.9"

        ##works but ..
        #sink_name="sink_name=ladspa_output.flanger_1191.flanger."+str(self.ladspa_index)
        #plugin = "plugin=flanger_1191"
        #label = "label=flanger"
        #control = "control=0,0,0,0"

        ## not working?
        #sink_name="sink_name=ladspa_output.df_flanger_1438.djFlanger."+str(self.ladspa_index)
        #plugin = "plugin=dj_flanger_1438"
        #label = "label=djFlanger"
        #control = "control=0,0,0,0"

        ## ..
        #sink_name="sink_name=ladspa_output.phasers_1217.autoPhaser."+str(self.ladspa_index)
        #plugin = "plugin=phasers_1217"
        #label = "label=autoPhaser"
        #control = "control=0,0,0,0,0"

        ## does not work
        #sink_name="sink_name=ladspa_output.dj_eq_1901.dj_eq."+str(self.ladspa_index)
        #plugin = "plugin=dj_eq_1901"
        #label = "label=dj_eq"
        #control = "control=0,0,0"

        ## no
        #sink_name="sink_name=ladspa_output.decay_1886.decay."+str(self.ladspa_index)
        #plugin = "plugin=decay_1886"
        #label = "label=decay"
        #control = "control=0"

        ## i dont hear it
        #sink_name="sink_name=ladspa_output.delay_1898.delay_n."+str(self.ladspa_index)
        #plugin = "plugin=delay_1898"
        #label = "label=delay_n"
        #control = "control=0,0"

        ## i dont hear it
        #sink_name="sink_name=ladspa_output.delay_1898.delay_l."+str(self.ladspa_index)
        #plugin = "plugin=delay_1898"
        #label = "label=delay_l"
        #control = "control=0,0"

        ## i dont hear it
        #sink_name="sink_name=ladspa_output.delay_1898.delay_c."+str(self.ladspa_index)
        #plugin = "plugin=delay_1898"
        #label = "label=delay_c"
        #control = "control=0,0"

        ## does not work (stereo)
        #sink_name="sink_name=ladspa_output.karaoke_1409.karaoke."+str(self.ladspa_index)
        #plugin = "plugin=karaoke_1409"
        #label = "label=karaoke"
        #control = "control=-50"

        ## not work (stereo)
        #sink_name="sink_name=ladspa_output.plate_1423.plate."+str(self.ladspa_index)
        #plugin = "plugin=plate_1423"
        #label = "label=plate"
        #control = "control=0,0,0"

        ## less fun
        #sink_name="sink_name=ladspa_output.pitch_scale_1194.pitchScaleHQ."+str(self.ladspa_index)
        #plugin = "plugin=pitch_scale_1194"
        #label = "label=pitchScaleHQ"
        #control = "control=1.9"


if __name__ == '__main__':
    for x in fetch_plugins():
        print(x["preset_name"])
        print(" labels:" + str(x["labels"]))
        print(" control: " + str(x["control"]))
        print(" range: " + str(x["range"]))
        print(" scale: " + str(x["scale"]))

