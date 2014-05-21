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

import datetime, urllib
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import *
from PyKDE4.plasma import Plasma
from PyKDE4.kdecore import i18n

from LabelSlider import MeterSlider
from MuteButton  import MuteButton
from ClickableMeter import ClickableMeter
from SinkChannelWidget import SinkChannelWidget
from veromixcommon.LADSPAEffects import LADSPAEffects
from veromixcommon.LADSPAEffects import LADSPAPresetLoader
from veromixcommon.Utils import *

class Channel(QGraphicsWidget):

    def __init__(self , parent):
        QGraphicsWidget.__init__(self)
        self.veromix = parent
        self.index = -1
        self.pa = parent.getPulseAudio()
        self.set_name("")
        self.deleted = True
        self.pa_sink = None
        self.extended_panel_shown = False
        self.extended_panel= None
        self.show_meter = True
        self.expander = None
        self.popup_menu = None
        self.card_settings = None
        self.menus = None
        self.port_actions = None

        self.double_click_filter = ChannelEventFilter(self)
        self.installEventFilter(self.double_click_filter)

        self.init()
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed,True))

    def init(self):
        self.layout = QGraphicsLinearLayout(Qt.Vertical)
        self.layout.setContentsMargins(2,2,2,0)
        self.setLayout(self.layout)
        self.initArrangement()
        self.composeArrangement()
        self.setAcceptDrops(True)
        self._on_upate_expander_enabled()

    def initArrangement(self):
        self.create_frame()
        self.create_panel()
        self.createMute()
        self.createMiddle()
        self.create_expander()

    def composeArrangement(self):
        self.layout.addItem(self.frame)
        self.frame_layout.addItem(self.panel)
        self.panel_layout.addItem(self.mute)
        self.panel_layout.addItem(self.middle)

    def create_frame(self):
        self.frame = Plasma.Frame()
        self.frame_layout = QGraphicsLinearLayout(Qt.Vertical)
        self.frame.setEnabledBorders (Plasma.FrameSvg.NoBorder)
        self.frame.setFrameShadow(Plasma.Frame.Plain)
        self.frame_layout.setContentsMargins(0,0,0,0)
        self.frame.setLayout(self.frame_layout)

    def create_panel(self):
        self.panel = QGraphicsWidget()
        self.panel_layout = QGraphicsLinearLayout(Qt.Horizontal)
        self.panel_layout.setContentsMargins(6,8,10,6)
        self.panel.setLayout(self.panel_layout)

    def createMute(self):
        self.mute = MuteButton(self)
        self.connect(self.mute, SIGNAL("clicked()"), self.on_mute_cb)

    def createMiddle(self):
        self.middle = QGraphicsWidget()
        self.middle_layout = QGraphicsLinearLayout(Qt.Vertical)
        #self.middle_layout.setContentsMargins(6,8,6,0)
        self.middle_layout.setContentsMargins(0,0,0,0)
        self.middle.setLayout(self.middle_layout)
        self.middle.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.createSlider()
        self.middle_layout.addItem(self.slider)

    def createSlider(self):
        self.slider = MeterSlider(None, self.veromix.is_slider_unit_value_visible())
        self.slider.installEventFilter(self.double_click_filter)
        self.slider.set_meter_visible(self.veromix.is_meter_visible())
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setMaximum(self.veromix.get_max_volume_value())
        self.slider.setMinimum(0)
        self.slider.volumeChanged.connect( self.on_slider_cb)

    def create_expander(self):
        self.expander = Plasma.IconWidget(self.panel)
        self.expander.setZValue(10)
        self.connect(self, SIGNAL("geometryChanged()"), self._resize_widgets)
        self.expander.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed))
        self.expander.clicked.connect(self.on_expander_clicked)
        self.expander.setSvg("widgets/arrows", "left-arrow")

    def create_context_menu(self, event):
        self.popup_menu = QMenu()
        self.popup_menu.triggered.connect(self.on_contextmenu_clicked)
        self.context_menu_create_custom()
        self.context_menu_create_mute()
        self.context_menu_create_meter()
        self.context_menu_create_unlock_channels()
        self.context_menu_create_effects()
        self.create_menu_kill_sink()
        self.context_menu_create_settings()
        if event:
            self.popup_menu.exec_(event.screenPos())
        else:
            self.popup_menu.exec_(QCursor.pos())

    def context_menu_create_mute(self):
        action_mute = QAction(i18n("Muted"), self.popup_menu)
        self.popup_menu.addAction(action_mute)
        action_mute.setCheckable(True)
        action_mute.setChecked(self.isMuted())
        action_mute.triggered.connect(self.on_mute_cb)

    def context_menu_create_meter(self):
        action_meter = QAction(i18n("Volume meter"), self.popup_menu)
        self.popup_menu.addAction(action_meter)
        action_meter.setCheckable(True)
        action_meter.setChecked(self.pa_sink.has_monitor())
        action_meter.triggered.connect(self.on_meter_cb)

    def context_menu_create_unlock_channels(self):
        action_unlock = QAction(i18n("Unlock channels"), self.popup_menu)
        self.popup_menu.addAction(action_unlock)
        action_unlock.setCheckable(True)
        action_unlock.setChecked(self.extended_panel_shown)
        action_unlock.triggered.connect(self.toggle_channel_lock)

    def context_menu_create_ports(self):
        self.port_actions = {}
        if len(self.pa_sink.ports.keys()) > 1:
            ports_menu = QMenu(i18n("Ports"), self.popup_menu)
            ports = self.pa_sink.ports

            for port in ports.keys():
                action = QAction(in_unicode(ports[port]), self.popup_menu)
                self.port_actions[action]=port
                if port == self.pa_sink.active_port:
                    action.setCheckable(True)
                    action.setChecked(True)
                else:
                    action.setChecked(False)
                    action.setCheckable(False)
                ports_menu.addAction(action)
            self.popup_menu.addMenu(ports_menu)

    def create_menu_kill_sink(self):
        pass

    def context_menu_create_sounddevices(self):
        self.card_settings = {}
        self.menus = []
        for card in self.veromix.card_infos.values():
            current = self.veromix.get_card_info_for(self)
            if current != None and  current.get_description() == card.get_description():
                card_menu = QMenu(i18n("Profile"), self.popup_menu)
                self.popup_menu.addMenu(card_menu)
            else:
                card_menu = QMenu(card.get_description(), self.popup_menu)
                self.menus.append(card_menu)
            active_profile_name = card.get_active_profile_name()
            self.profiles = card.get_profiles()
            for profile in self.profiles:
                action = QAction(in_unicode(profile.description), card_menu)
                self.card_settings[action] = card
                if profile.name == active_profile_name:
                    action.setCheckable(True)
                    action.setChecked(True)
                card_menu.addAction(action)

    def context_menu_create_sounddevices_other(self):
        if len(self.menus) > 0:
            self.popup_menu.addSeparator()
            for each in self.menus:
                self.popup_menu.addMenu(each)

    def context_menu_create_custom(self):
        pass

    def context_menu_create_effects(self):
        pass

    def context_menu_create_settings(self):
        self.popup_menu.addSeparator()
        action_settings = QAction(i18n("Veromix Settings"), self.popup_menu)
        self.popup_menu.addAction(action_settings)
        action_settings.triggered.connect(self.veromix.applet.showConfigurationInterface)

    def _resize_widgets(self):
        self.expander.setPos(int(self.panel.size().width() - self.expander.size().width()) ,0)

    def on_double_clicked(self):
        self.slider.toggle_meter()
        self.pa_sink.toggle_monitor()
        self.slider.set_meter_value(0)

    def on_step_volume(self, up):
        vol = self.pa_sink.get_volume()
        STEP = 5
        if up:
            vol = vol + STEP
        else:
            vol = vol - STEP
        if vol < 0:
            vol = 0
        if vol > self.veromix.get_max_volume_value():
            vol = self.veromix.get_max_volume_value()
        self.setVolume(vol)

    def setVolume(self, value):
        vol = self.pa_sink.volumeDiffFor(value)
        if self.veromix.get_auto_mute():
            for c in vol:
                if c <= 0:
                    ## FIXME HACK for MurzNN this should be conditional
                    self.pa.set_sink_mute(self.index, True)
                    self.automatically_muted = True
                    return
            if self.automatically_muted :
                self.automatically_muted = False
                self.pa.set_sink_mute(self.index, False)
        self.set_channel_volumes(vol)

    def get_volume(self):
        if self.pa_sink:
            return self.pa_sink.get_volume()
        return [0]

    def on_expander_clicked(self):
        self.contextMenuEvent(None)

    def toggle_channel_lock(self):
        self.middle_layout.removeItem(self.slider)
        self.slider = None
        if (self.extended_panel_shown):
            self.extended_panel_shown = False
            self.expander.setSvg("widgets/arrows", "left-arrow")
            self.createSlider()
            self.middle_layout.addItem(self.slider)
        else:
            self.extended_panel_shown = True
            self.expander.setSvg("widgets/arrows", "down-arrow")
            self.slider = SinkChannelWidget(self.veromix, self)
            self.slider.installEventFilter(self.double_click_filter)
            self.middle_layout.addItem(self.slider)
        self.middle_layout.setContentsMargins(0,0,0,0)
        self.middle.setContentsMargins(0,0,0,0)
        self.update_with_info(self.pa_sink)
        self.veromix.check_geometries()

    def on_update_configuration(self):
        self.slider.set_meter_visible(self.veromix.is_meter_visible())
        self.slider.setMaximum(self.veromix.get_max_volume_value())
        self.slider.set_unit_value_visible(self.veromix.is_slider_unit_value_visible())
        self._on_upate_expander_enabled()

    def _on_upate_expander_enabled(self):
        if self.veromix.is_expander_enabled():
            self.expander.show()
        else:
            self.expander.hide()

    def on_contextmenu_clicked(self, action):
        if action in self.card_settings.keys():
            card = self.card_settings[action]
            for profile in card.get_profiles():
                if action.text() == profile.description:
                    self.veromix.pa.set_card_profile(card.index, profile.name)
        if action in self.port_actions.keys():
            self.pa_sink.set_port(self.port_actions[action])

    def contextMenuEvent(self,event):
        self.create_context_menu(event)

    def on_mute_cb(self):
        self.pa_sink.toggle_mute()

    def on_meter_cb(self):
        self.on_double_clicked()

    def sink_input_kill(self):
        self.pa_sink.kill()

    def set_channel_volumes(self, values):
        self.pa_sink.set_volume(values)

    def on_update_meter(self, index, value, number_of_sinks):
        if self.index == index:
            self.slider.set_meter_value(int(value))

    def update_with_info(self,info):
        self.pa_sink = info
        self.index = info.index
        self.update_label()
        self.updateIcon()
        if self.slider:
            self.slider.update_with_info(info)
        if self.extended_panel:
            self.extended_panel.update_with_info(info)
        self.update()

    def update_label(self):
        if self.pa_sink:
            self.set_name(self.pa_sink.name)

    def getOutputIndex(self):
        return self.index

    def sinkIndexFor( self, index):
        return (index * 100000) + 100000

    def updateIcon(self):
        pass

    def on_slider_cb(self, value):
        self.setVolume(value)

    def isDefaultSink(self):
        if self.pa_sink and "isdefault" in self.pa_sink.props:
            return self.pa_sink.props["isdefault"] == "True"
        return False

    def startDrag(self,event):
        pass

    def removeSlider(self):
        # if a slider is not visible, plasmoidviewer crashes if the slider is not removed.. (dont ask me)
        if self.slider:
            self.middle_layout.removeItem(self.slider)
        self.slider = None

    def isMuted(self):
        if self.pa_sink:
            return self.pa_sink.isMuted()
        return False

    def isSinkOutput(self):
        if self.pa_sink:
            return self.pa_sink.is_sinkoutput()
        return False

    def isSinkInput(self):
        if self.pa_sink:
            return self.pa_sink.is_sinkinput()
        return False

    def isSink(self):
        if self.pa_sink:
            return self.pa_sink.is_sink()
        return False

    def isNowplaying(self):
        return False

    def isSourceOutput(self):
        if self.pa_sink:
            return self.pa_sink.is_sourceoutput()
        return False

    def wheelEvent(self, event):
        if self.slider:
            self.slider.wheelEvent(event)

    def set_name(self, string):
        self._name = in_unicode(string)

    def name(self):
        return self._name

    def update_module_info(self, index, name, argument, n_used, auto_unload):
        pass

    def get_ladspa_type(self):
        return str(type(self))

    def get_pasink_name(self):
        return self.pa_sink.name

## LADSPA helpers

    def populate_presets_menu(self, target_menu, checked_item, add_actions):
        effect_menu = QMenu(i18n("Presets"), target_menu)
        if add_actions:
            self.action_save_preset = QAction(i18n("Save"),effect_menu)
            effect_menu.addAction(self.action_save_preset)
            if not self.is_preset():
                self.action_save_preset.setEnabled(False)

            self.action_save_as_preset = QAction(i18n("Save As..."),effect_menu)
            effect_menu.addAction(self.action_save_as_preset)
            effect_menu.addSeparator()

        for preset in LADSPAPresetLoader().presets():
            action = QAction(preset["preset_name"],effect_menu)
            effect_menu.addAction(action)
            if checked_item == preset["preset_name"]:
                action.setCheckable(True)
                action.setChecked(True)
                action.setEnabled(False)
        target_menu.addMenu(effect_menu)

    def populate_switch_effect_menu(self, target_menu, checked_item):
        effect_menu = QMenu(i18n("Effect"), target_menu)
        for preset in LADSPAEffects().effects():
            action = QAction(preset["preset_name"],effect_menu)
            effect_menu.addAction(action)
            if checked_item == preset["label"]:
                action.setCheckable(True)
                action.setChecked(True)
                action.setEnabled(False)
        target_menu.addMenu(effect_menu)

    def on_set_ladspa_effect(self, value, master):
        parameters = ""
        preset = None
        for p in LADSPAEffects().effects():
            if p["preset_name"] == value:
                parameters = "sink_name=" + urllib.quote(p["name"])
                preset = p

        for p in LADSPAPresetLoader().presets():
            if p["preset_name"] == value:
                parameters = "sink_name=" + urllib.quote(p["preset_name"])
                preset = p

        parameters =  parameters + " master=" + master + " "
        parameters =  parameters + " plugin=" + preset["plugin"]
        parameters =  parameters + " label=" + preset["label"]
        parameters =  parameters + " control=" + preset["control"]
        self.pa_sink.set_ladspa_sink(parameters)

    def next_focus(self, forward=True):
        channels = self.veromix.get_visible_channels()
        if len(channels) > 0:
            index = 0
            if self in channels:
                index = channels.index(self)
                if forward:
                    index = index + 1
                    if index >= len(channels):
                        index = 0
                else:
                    index = index - 1
                    if index < 0:
                        index = len(channels) - 1
            channels[index].set_focus()

    def set_focus(self):
        self.slider.set_focus()

    def pa_sink_proxy(self):
        return self.pa_sink

class ChannelEventFilter(QObject):
    def __init__(self, channel):
        QObject.__init__(self)
        self.channel = channel

    def eventFilter(self, obj, event):
        if event and event.type() == QEvent.GraphicsSceneMouseDoubleClick:
            self.channel.on_double_clicked()
            return True

        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Backtab:
                self.channel.next_focus(False)
                return True
            elif event.key() == Qt.Key_Tab:
                self.channel.next_focus()
                return True
        return QObject.eventFilter(self, obj, event)

