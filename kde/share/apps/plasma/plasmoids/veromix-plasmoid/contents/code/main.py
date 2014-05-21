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

###
# Veromix  - A Pulseaudio volume control
#
# Veromix has two components:
# - a service that sends notifications over dbus and offers an interface
#   to perform actions (set volume, mute ...)
# - the plasmoid that connects to the service
#
# The service is launchd by dbus. For this to work veromix installs a service
# description-file in /usr/share/dbus-1/services/ called org.veromix.pulseaudio.service .
#
# Pulseaudio will (one day) provide their own dbus-interface:
# http://pulseaudio.org/wiki/DBusInterface
#
# The python-interface to pulseaudio is a mix of these two projects (extended by myself):
# https://launchpad.net/earcandy
# https://fedorahosted.org/pulsecaster/
###### 2009 - 2012


import commands,dbus

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from PyKDE4 import plasmascript
from PyKDE4.plasma import Plasma
from PyKDE4.kdeui import KIcon
from PyKDE4.kdeui import KActionCollection
from PyKDE4.kdeui import KAction
from PyKDE4.kdeui import KShortcut
from PyKDE4.kdeui import KKeySequenceWidget
from PyKDE4.kdeui import KPageDialog
from PyKDE4.kdeui import KDialog
from PyKDE4.kdecore import *

from VeroMix import VeroMix
from NowPlaying import NowPlayingController
from veromixcommon.LADSPAEffects import LADSPAEffects
from veromixcommon.LADSPAEffects import LADSPAPresetLoader
from veromixcommon.Utils import *

COMMENT=i18n("Veromix is a mixer for the Pulseaudio sound server. ")

class VeroMixPlasmoid(plasmascript.Applet):
    VERSION="0.18.3"

    nowplaying_player_added = pyqtSignal(QString, QObject)
    nowplaying_player_removed = pyqtSignal(QString)
    nowplaying_player_dataUpdated = pyqtSignal(QString, dict)

    def __init__(self,parent,args=None):
        self.engine = None
        self.now_playing_engine = None
        self.louder_action_editor = None
        self.lower_action_editor = None
        self.mute_action_editor = None
        self.card_settings = None
        self.messageDialog = None
        self.messageOverlay = None
        self.config_ui = None
        plasmascript.Applet.__init__(self,parent)

    def init(self):
        plasmascript.Applet.init(self)
        KGlobal.locale().insertCatalog("veromix");
        if "usr/share/kde4" not in os.path.realpath(__file__):
            out = commands.getstatusoutput("xdg-icon-resource install --size 128 " + unicode(self.package().path()) + "contents/icons/veromix-plasmoid-128.png veromix-plasmoid")
            if out[0] == 0:
                print "veromix icon installed"
            else:
                print "Error installing veromix icon:", out

        LADSPAPresetLoader().install_ladspa_presets_if_needed()
        if self.is_ladspa_enabled():
            # force singleton initialisation
            LADSPAPresetLoader().presets()
            LADSPAEffects().effects()

        createDbusServiceDescription(self.package().path() + "/dbus-service/veromix-service-qt.py", True)

        KGlobal.locale().insertCatalog("veromix")

        self.setHasConfigurationInterface(True)
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
        self.theme = Plasma.Svg(self)

        self.widget = VeroMix(self)
        self.widget.init()

        defaultSize =  QVariant(QSize (0,0))
        size = self.config().readEntry("size", defaultSize).toSize()
        if self.formFactor() == Plasma.Planar:
            self.widget.setMinimumSize(275,125)
        elif (size != defaultSize) :
            self.widget.setPreferredSize(size.width(), size.height())
        else:
            self.widget.setPreferredSize(470 ,145)

        self.connect(self.widget, SIGNAL("resized()"), self.dialogResized)
        #try:
        self.setGraphicsWidget(self.widget)
        self.applet.setPassivePopup(True)
        ## FIXME: see fixPopupcion
        self.setPopupIcon(KIcon("audio-volume-high"))
        #self.setPopupIcon("audio-volume-muted")
        # dont know why but adding it a second time helps (otherwise it
        # wont popup when you add it directly to the panel)
        self.setGraphicsWidget(self.widget)
        self.connect(self.applet, SIGNAL("appletDestroyed(Plasma::Applet*)"), self.doExit)
        self.setBackgroundHints(Plasma.Applet.StandardBackground)
        self.applyConfig()
        #except AttributeError , e:
            #print e
            #updateMetadataDesktop(self)

        self.initTooltip()
        self.initShortcuts()
        QTimer.singleShot(1000, self.fixPopupIcon)

    def initShortcuts(self):
        self.actionCollection = KActionCollection(self)
        #self.actionCollection.setConfigGlobal(True)
        self.louder_action = self.actionCollection.addAction("VeromixVolumeUp")
        self.louder_action.setText( i18n("Veromix volume up"))
        self.louder_action.setGlobalShortcut(KShortcut())
        self.louder_action.triggered.connect(self.widget.on_step_volume_up)

        self.lower_action = self.actionCollection.addAction("VeromixVolumeDown")
        self.lower_action.setText(i18n("Veromix volume down"))
        self.lower_action.setGlobalShortcut(KShortcut())
        self.lower_action.triggered.connect(self.widget.on_step_volume_down)

        self.mute_action = self.actionCollection.addAction("VeromixVolumeMute")
        self.mute_action.setText(i18n("Veromix toggle mute"))
        self.mute_action.setGlobalShortcut(KShortcut())
        self.mute_action.triggered.connect(self.widget.on_toggle_mute)

    def initTooltip(self):
        if (self.formFactor() != Plasma.Planar):
            self.tooltip = Plasma.ToolTipContent()
            self.tooltip.setImage(pixmapFromSVG("audio-volume-high"))
            self.tooltip.setMainText(i18n( "Main Volume"))
            #self.tooltip.setSubText("")
            Plasma.ToolTipManager.self().setContent(self.applet, self.tooltip)
            Plasma.ToolTipManager.self().registerWidget(self.applet)

    def updateIcon(self):
        icon_state = "audio-volume-muted"
        sink = self.widget.getDefaultSink()
        if sink == None:
            QTimer.singleShot(2000, self.fixPopupIcon)
            return
        vol = sink.get_volume()
        if sink.isMuted() :
            icon_state= "audio-volume-muted"
        else:
            if  vol == 0:
                icon_state = "audio-volume-muted"
            elif vol < 30:
                icon_state= "audio-volume-low"
            elif vol < 70:
                icon_state= "audio-volume-medium"
            else:
                icon_state= "audio-volume-high"
        self.setPopupIcon(icon_state)
        if (self.formFactor() != Plasma.Planar):
            self.tooltip.setImage(pixmapFromSVG(icon_state))
            ## FIXME this should better go to toolTipAboutToShow but is not working:
            # https://bugs.kde.org/show_bug.cgi?id=254764
            self.tooltip.setMainText(sink.name())
            self.tooltip.setSubText( str(vol) + "%")
            Plasma.ToolTipManager.self().setContent(self.applet, self.tooltip)

    def showTooltip(self):
        if self.get_show_toolip():
            Plasma.ToolTipManager.self().show(self.applet)

    @pyqtSlot(name="toolTipAboutToShow")
    def toolTipAboutToShow(self):
        pass

    ## FIXME Looks like a bug in plasma: Only when sending a
    # KIcon instance PopUpApplet acts like a Poppupapplet...
    def fixPopupIcon(self):
        #sink = self.widget.getDefaultSink()
        #if sink:
        self.updateIcon()

    def doExit(self):
        # prevent crash in plasmoidviewer
        self.widget.doExit()
        self.widget.deleteLater()

    def dialogResized(self):
        if self.isPopupShowing():
            self.config().writeEntry("size", QVariant(self.widget.size()))

    def query_application(self, query):
        #print "query: ", query
        if not query :
            return None
        needle = query.lower()
        if self.engine == None:
            self.engine = self.dataEngine("apps")
        for source in self.engine.sources():
            key = unicode(source).replace(".desktop", "")
            if  (0<=  key.find(needle)) or  (0 <= needle.find(key))  :
                #print "found: ",key,  needle , source
                result = self.engine.query(source)
                if QString("iconName") in result:
                    iconname = result[QString("iconName")].toString()
                    return iconname
        return None

    def wheelEvent(self, event):
        if event.orientation() == Qt.Horizontal:
            self.widget.on_step_volume((event.delta() < 0))
        else:
            self.widget.on_step_volume((event.delta() > 0))

    def mousePressEvent(self, event):
        if event.button() == Qt.MidButton:
            self.widget.on_toggle_mute()

    def createConfigurationInterface(self, parent):
        self.pp = parent
        self.config_widget = QWidget(parent)
        self.connect(self.config_widget, SIGNAL('destroyed(QObject*)'), self.configWidgetDestroyed)

        self.config_ui = uic.loadUi(str(self.package().filePath('ui', 'appearance.ui')), self.config_widget)
        self.config_ui.showBackground.setCurrentIndex( self.config().readEntry("background","2").toInt() [0])
        self.config_ui.showBackground.currentIndexChanged.connect(parent.settingsModified)
        if self.formFactor() != Plasma.Planar:
            self.config_ui.showBackground.setEnabled(False)

        self.config_ui.popupMode.setCurrentIndex( self.config().readEntry("popupMode",False).toInt() [0])
        self.config_ui.popupMode.currentIndexChanged.connect(parent.settingsModified)
        if self.formFactor() == Plasma.Planar:
            self.config_ui.popupMode.setEnabled(False)

        self.config_ui.useTabs.setChecked(self.useTabs())
        self.config_ui.useTabs.stateChanged.connect(parent.settingsModified)

        self.config_ui.show_tooltip.setChecked(self.get_show_toolip())
        self.config_ui.show_tooltip.stateChanged.connect(parent.settingsModified)

        self.config_ui.always_show_sources.setChecked(self.get_always_show_sources())
        self.config_ui.always_show_sources.stateChanged.connect(parent.settingsModified)

        self.config_ui.meter_visible.setChecked(self.is_meter_visible())
        self.config_ui.meter_visible.stateChanged.connect(parent.settingsModified)

        self.config_ui.expander_enabled.setChecked(self.is_expander_enabled())
        self.config_ui.expander_enabled.stateChanged.connect(parent.settingsModified)

        self.config_ui.unitvalues_visible.setChecked(self.is_slider_unit_value_visible())
        self.config_ui.unitvalues_visible.stateChanged.connect(parent.settingsModified)

        self.config_ui.version.setText(VeroMixPlasmoid.VERSION)
        parent.addPage(self.config_widget, i18n("Appearance"), "veromix")

        self.mediaplayer_settings_widget = QWidget(parent)
        self.mediaplayer_settings_ui = uic.loadUi(str(self.package().filePath('ui', 'nowplaying.ui')), self.mediaplayer_settings_widget)

        self.mediaplayer_settings_ui.mediaplayerBlacklist.setPlainText(self.get_mediaplayer_blacklist_string())
        self.mediaplayer_settings_ui.runningMediaplayers.setPlainText(self.get_running_mediaplayers())
        self.mediaplayer_settings_ui.runningMediaplayers.setReadOnly(True)

        self.mediaplayer_settings_ui.use_nowplaying.setChecked(self.is_nowplaying_enabled())
        self.mediaplayer_settings_ui.use_nowplaying.stateChanged.connect(self.update_mediaplayer_settings_ui)
        self.mediaplayer_settings_ui.use_nowplaying.stateChanged.connect(parent.settingsModified)

        self.mediaplayer_settings_ui.use_mpris2.setChecked(self.is_mpris2_enabled())
        self.mediaplayer_settings_ui.use_mpris2.stateChanged.connect(self.update_mediaplayer_settings_ui)
        self.mediaplayer_settings_ui.use_mpris2.stateChanged.connect(parent.settingsModified)

        self.mediaplayer_settings_ui.show_albumart.setChecked(self.is_albumart_enabled())
        self.mediaplayer_settings_ui.show_albumart.stateChanged.connect(parent.settingsModified)

        parent.addPage(self.mediaplayer_settings_widget, i18n("Media Player Controls"), "veromix")

        #self.about_widget = QWidget(parent)
        #self.about_ui = uic.loadUi(str(self.package().filePath('ui', 'about.ui')), self.about_widget)
        #self.about_ui.version.setText(VeroMixPlasmoid.VERSION)
        #parent.addPage(self.about_widget, "About", "help-about")
        self.add_audio_settings(parent)
        self.add_ladspa_settings(parent)
        self.add_global_shortcut_page(parent)

        # FIXME KDE 4.6 workaround
        self.connect(parent, SIGNAL("okClicked()"), self.configChanged)
        self.connect(parent, SIGNAL("applyClicked()"), self.configChanged)
        self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)
        return self.config_widget

    def add_audio_settings(self, dialog):
        self.audio_settings_page = QWidget()
        layout = QGridLayout()
        self.audio_settings_page.setLayout(layout)

        self.max_volume_spinbox = QSpinBox()
        self.max_volume_spinbox.setRange(1,255)
        self.max_volume_spinbox.setSingleStep(1)
        self.max_volume_spinbox.setValue(self.get_max_volume_value())
        self.max_volume_spinbox.valueChanged.connect(dialog.settingsModified)
        layout.addWidget(QLabel(i18n("Max volume value")), 0,0)
        layout.addWidget(self.max_volume_spinbox, 0,1)

        self.automute_checkbox = QCheckBox()
        self.automute_checkbox.setChecked(self.get_auto_mute())
        self.automute_checkbox.stateChanged.connect(dialog.settingsModified)
        layout.addWidget(QLabel(i18n("Mute if volume reaches zero")), 1,0)
        layout.addWidget(self.automute_checkbox, 1,1)

        layout.addItem(QSpacerItem(0,20, QSizePolicy.Minimum,QSizePolicy.Fixed), 2,0)
        layout.addWidget(QLabel("<b>"+i18n("Sound Card Profiles")+"</b>"), 3,0)
        index=4
        self.card_settings = {}
        for card in self.widget.card_infos.values():
            combo = QComboBox()
            #self.automute_checkbox.setChecked(self.get_auto_mute())
            #print card.properties
            layout.addWidget(QLabel(card.properties[dbus.String("device.description")]), index,0)
            layout.addWidget(combo, index,1)
            index = index + 1

            self.card_settings[combo] = card
            profiles = card.get_profiles()
            active = card.get_active_profile_name()
            active_index = 0
            for profile in profiles:
                combo.addItem(profile.description)
                if active == profile.name:
                    active_index = profiles.index(profile)
            combo.setCurrentIndex(active_index)

        layout.addItem(QSpacerItem(0,0, QSizePolicy.Minimum,QSizePolicy.Expanding), index,0)
        dialog.addPage(self.audio_settings_page, i18n("Pulseaudio"), "preferences-desktop-sound")

    def add_ladspa_settings(self, dialog):
        self.ladspa_settings_page = QWidget()
        layout = QGridLayout()
        self.ladspa_settings_page.setLayout(layout)

        text = i18n("LADSPA is a standard for handling audio filters and effects. Every linux software archive offers a large number of effects - search for LADSPA to get more.\
            Not every effect is supported by Pulseaudio and others simple don't make sense (or create only noise).<br/><br/>\
            The following list shows all available effects on your system: Only checked effects will appear in the context-menu.")

        if not LADSPAEffects().ladspa_sdk_available():
            text = text + i18n("<br/><br/><b>Warning:</b> Cannot find the executables 'listplugins' and 'analyseplugin' which are required for dynamically detecting installed effects.<br/>\
               In OpenSUSE, Fedora and Arch Linux the package is named 'ladspa', in Debian/Ubuntu 'ladspa-sdk'.<br/><br/>")

        ladspa_intro = QLabel(text)

        ladspa_intro.setWordWrap(True)
        layout.addWidget(ladspa_intro, 0,0)

        self.ladspa_enabled_checkbox = QCheckBox()
        self.ladspa_enabled_checkbox.setText(i18n("Enable LADSPA effects."))
        self.ladspa_enabled_checkbox.setChecked(self.is_ladspa_enabled())
        self.ladspa_enabled_checkbox.stateChanged.connect(dialog.settingsModified)
        layout.addWidget(self.ladspa_enabled_checkbox, 1,0)

        self.effects_list_widget = QListWidget()
        layout.addWidget(self.effects_list_widget,2,0)
        self.effects_list_widget.itemClicked.connect(dialog.settingsModified)

        blacklisted = LADSPAEffects().blacklist()
        effects = LADSPAEffects().all_effects()
        for effect in effects:
            item = QListWidgetItem(effect["preset_name"])
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            if effect["preset_name"] in blacklisted:
                item.setCheckState(Qt.Unchecked)
            else:
                item.setCheckState(Qt.Checked)
            self.effects_list_widget.addItem(item)

        layout.addItem(QSpacerItem(0,0, QSizePolicy.Minimum,QSizePolicy.Expanding), 3,0)
        dialog.addPage(self.ladspa_settings_page, i18n("Effects / Equalizer"), "preferences-desktop-sound")

    # anybody knows how to remove/extend the default shortcuts page?
    def add_global_shortcut_page(self,dialog):
        self.kb_settings_page = QWidget()

        layout = QGridLayout()
        self.kb_settings_page.setLayout(layout)

        self.louder_action_editor = KKeySequenceWidget()
        self.louder_action_editor.setKeySequence( self.louder_action.globalShortcut().primary())
        layout.addWidget(QLabel(i18n("Veromix volume up")), 0,0)
        layout.addWidget(self.louder_action_editor, 0,1)

        self.lower_action_editor = KKeySequenceWidget()
        self.lower_action_editor.setKeySequence( self.lower_action.globalShortcut().primary())
        layout.addWidget(QLabel(i18n("Veromix volume down")), 1, 0)
        layout.addWidget(self.lower_action_editor, 1, 1)

        self.mute_action_editor = KKeySequenceWidget()
        self.mute_action_editor.setKeySequence( self.mute_action.globalShortcut().primary())
        layout.addWidget(QLabel(i18n("Veromix toggle  mute")), 2, 0)
        layout.addWidget(self.mute_action_editor, 2, 1)

        layout.addItem(QSpacerItem(0,0, QSizePolicy.Minimum,QSizePolicy.Expanding), 3,0)
        dialog.addPage(self.kb_settings_page, i18n("Volume Keyboard Shortcuts"), "preferences-desktop-keyboard")

    def configDenied(self):
        self.apply_nowplaying(self.is_nowplaying_enabled())
        self.apply_mpris2(self.is_mpris2_enabled())

    def configChanged(self):
        if self.config_ui:
            self.config().writeEntry("background",str(self.config_ui.showBackground.currentIndex()))
            self.config().writeEntry("popupMode", str(self.config_ui.popupMode.currentIndex()))
            tabs = self.useTabs()
            self.config().writeEntry("useTabs", bool(self.config_ui.useTabs.isChecked()))
            self.config().writeEntry("show_tooltip", bool(self.config_ui.show_tooltip.isChecked()))
            self.config().writeEntry("always_show_sources", bool(self.config_ui.always_show_sources.isChecked()))

            self.config().writeEntry("meter_visible", bool(self.config_ui.meter_visible.isChecked()))
            self.config().writeEntry("expander_enabled", bool(self.config_ui.expander_enabled.isChecked()))
            self.config().writeEntry("unitvalues_visible", bool(self.config_ui.unitvalues_visible.isChecked()))

            self.config().writeEntry("use_nowplaying", str(self.mediaplayer_settings_ui.use_nowplaying.isChecked()))
            self.config().writeEntry("use_mpris2", str(self.mediaplayer_settings_ui.use_mpris2.isChecked()))
            self.config().writeEntry("show_albumart", str(self.mediaplayer_settings_ui.show_albumart.isChecked()))

            #self.config().writeEntry("mpris2List",str(self.mediaplayer_settings_ui.mpris2List.toPlainText()).strip())
            self.config().writeEntry("nowplayingBlacklist",str(self.mediaplayer_settings_ui.mediaplayerBlacklist.toPlainText()).strip())

            self.config().writeEntry("max_volume", str(self.max_volume_spinbox.value()))
            self.config().writeEntry("auto_mute", str(self.automute_checkbox.isChecked()))

            self.config().writeEntry("ladspa_enabled",str(self.ladspa_enabled_checkbox.isChecked()))
            self.ladspa_save_effects_blacklist()
            if tabs != self.useTabs():
                self.widget.switchView()
        self.applyConfig()
        self.widget.on_update_configuration()

    def update_mediaplayer_settings_ui(self):
        enable = ( self.mediaplayer_settings_ui.use_nowplaying.isChecked() or self.mediaplayer_settings_ui.use_mpris2.isChecked())
        self.mediaplayer_settings_ui.mediaplayerBlacklist.setEnabled(enable)
        self.mediaplayer_settings_ui.mediaplayerBlacklistLabel.setEnabled(enable)
        self.mediaplayer_settings_ui.runningMediaplayers.setEnabled(enable)
        self.mediaplayer_settings_ui.runningMediaplayersLabel.setEnabled(enable)
        self.mediaplayer_settings_ui.runningMediaplayers.setPlainText(self.get_running_mediaplayers())
        self.mediaplayer_settings_ui.show_albumart.setEnabled(enable)

    def apply_nowplaying(self, enabled):
        self.disable_nowplaying()
        if enabled:
            self.init_nowplaying()

    def apply_mpris2(self, enabled):
        self.widget.pa.disable_mpris2()
        self.remove_mpris2_widgets()
        if enabled:
            self.widget.pa.enable_mpris2()
            self.init_running_mpris2()

    def applyConfig(self):
        self.apply_nowplaying(self.is_nowplaying_enabled())
        self.apply_mpris2(self.is_mpris2_enabled())

        if self.formFactor() == Plasma.Planar:
            bg = self.config().readEntry("background","2").toInt()[0]
            if bg == 0:
                self.setBackgroundHints(Plasma.Applet.NoBackground)
            elif bg == 1:
                self.setBackgroundHints(Plasma.Applet.TranslucentBackground)
            else:
                self.setBackgroundHints(Plasma.Applet.StandardBackground)

        mode = self.config().readEntry("popupMode",False).toInt()[0]
        if  mode== 0:
            self.setPassivePopup(False)
        elif mode == 1:
            self.setPassivePopup(True)
        else:
            self.setPassivePopup(True)

        if self.louder_action_editor:
            sequence = self.louder_action_editor.keySequence()
            if sequence != self.louder_action.globalShortcut().primary():
                self.louder_action.setGlobalShortcut(KShortcut(sequence), KAction.ActiveShortcut, KAction.NoAutoloading)
        if self.lower_action_editor:
            sequence = self.lower_action_editor.keySequence()
            if sequence != self.lower_action.globalShortcut().primary():
                self.lower_action.setGlobalShortcut(KShortcut(sequence), KAction.ActiveShortcut, KAction.NoAutoloading)
        if self.mute_action_editor:
            sequence = self.mute_action_editor.keySequence()
            if sequence != self.mute_action.globalShortcut().primary():
                self.mute_action.setGlobalShortcut(KShortcut(sequence), KAction.ActiveShortcut, KAction.NoAutoloading)

        if self.card_settings:
            for combo in self.card_settings.keys():
                card = self.card_settings[combo]
                for profile in card.profiles:
                    if combo.currentText() == profile.description:
                        self.widget.pa.set_card_profile(card.index, profile.name)

        self.update()

    def configWidgetDestroyed(self):
        self.config_widget = None
        self.config_ui = None

    def useTabs(self):
        return self.config().readEntry("useTabs",False).toBool()

    def is_meter_visible(self):
        return self.config().readEntry("meter_visible",False).toBool()

    def get_auto_mute(self):
        return self.config().readEntry("auto_mute",False).toBool()

    def get_show_toolip(self):
        return self.config().readEntry("show_tooltip",True).toBool()

    def get_always_show_sources(self):
        return self.config().readEntry("always_show_sources",False).toBool()

    def get_max_volume_value(self):
        default = 100
        return self.config().readEntry("max_volume",default).toInt()[0]

    def is_slider_unit_value_visible(self):
        return self.config().readEntry("unitvalues_visible",False).toBool()

    def is_ladspa_enabled(self):
        return self.config().readEntry("ladspa_enabled",True).toBool()

    def ladspa_save_effects_blacklist(self):
        blacklisted = []
        for i in range(0,self.effects_list_widget.count()):
            item = self.effects_list_widget.item(i)
            if not item.checkState():
                blacklisted.append(str(item.text()))
        LADSPAEffects().write_blacklist(blacklisted)

### now playing

    def is_nowplaying_enabled(self):
        return self.config().readEntry("use_nowplaying",False).toBool()

    def is_mpris2_enabled(self):
        return self.config().readEntry("use_mpris2",True).toBool()

    def is_albumart_enabled(self):
        return self.config().readEntry("show_albumart",True).toBool()

    def is_expander_enabled(self):
        return self.config().readEntry("expander_enabled",True).toBool()

    def disable_nowplaying(self):
        for player in self.widget.get_mediaplayer_widgets():
            if player.is_nowplaying_player():
                self.on_nowplaying_player_removed(player.controller_name())
        self.now_playing_engine = None

    def remove_mpris2_widgets(self):
        for player in self.widget.get_mediaplayer_widgets():
            if player.is_mpris2_player():
                self.on_mpris2_removed(player.controller_name())

    def init_nowplaying(self):
        self.now_playing_engine = self.dataEngine('nowplaying')
        self.connect(self.now_playing_engine, SIGNAL('sourceAdded(QString)'), self.on_nowplaying_player_added)
        self.connect(self.now_playing_engine, SIGNAL('sourceRemoved(QString)'), self.on_nowplaying_player_removed)
        self.connect_to_nowplaying_engine()

    def init_running_mpris2(self):
        for controller in self.widget.pa.get_mpris2_players():
            v= controller.name()
            if self.in_mediaplayer_blacklist(v):
                return
            self.nowplaying_player_added.emit(controller.name(), controller)

    def connect_to_nowplaying_engine(self):
        # get sources and connect
        for source in self.now_playing_engine.sources():
            self.on_nowplaying_player_added(source)

    def on_nowplaying_player_added(self, player):
        if player == "players":
            # FIXME 4.6 workaround
            return
        if self.in_mediaplayer_blacklist(player):
            return
        self.now_playing_engine.disconnectSource(player, self)
        self.now_playing_engine.connectSource(player, self, 2000)
        controller = self.now_playing_engine.serviceForSource(player)
        self.nowplaying_player_added.emit(player, NowPlayingController(self.widget,controller))

    def in_mediaplayer_blacklist(self,player):
        for entry in self.get_mediaplayer_blacklist():
            if str(player).find(entry) == 0:
                return True
        return False

    def on_nowplaying_player_removed(self, player):
        if self.now_playing_engine:
            self.now_playing_engine.disconnectSource(player, self)
            self.nowplaying_player_removed.emit(player)

    def on_mpris2_removed(self, player):
        self.nowplaying_player_removed.emit(player)

    def get_running_mediaplayers(self):
        val = "nowplaying:\n"
        engine =  self.now_playing_engine
        if engine == None:
            engine = self.dataEngine('nowplaying')
        for source in engine.sources():
            val += source + "\n"
        val += "\nmpris2:\n"
        for controller in self.widget.pa.get_mpris2_players():
            val += controller.name() + "\n"
        return val

    def get_mediaplayer_blacklist(self):
        return self.get_mediaplayer_blacklist_string().split("\n")

    def get_mediaplayer_blacklist_string(self):
        default =  "org.mpris.bangarang"
        return self.config().readEntry("nowplayingBlacklist",default).toString()

    @pyqtSignature('dataUpdated(const QString&, const Plasma::DataEngine::Data&)')
    def dataUpdated(self, sourceName, data):
        self.nowplaying_player_dataUpdated.emit(sourceName, data)

## Modal Widget

    def showModalWidget(self,mainWidget):
        #mainWidget.widgetClose.connect(self.destroyMessageOverlay)
        if self.messageOverlay:
            return
        if self.messageDialog:
            return

        corona = self.scene()
        mainWidget.adjustSize()
        hint = mainWidget.preferredSize()
        if (hint.height() > self.widget.size().height()) or (hint.width() > self.widget.size().width()):
            ## either a collapsed popup in h/v form factor or just too small,
            ## so show it in a dialog associated with ourselves
            #pass
            if (corona):
                corona.addOffscreenWidget(mainWidget)

            if (self.messageDialog):
                pass
            else:
                self.messageDialog = Plasma.Dialog()

            self.messageDialog.setGraphicsWidget(mainWidget)
            mainWidget.setParentItem(self.messageDialog.graphicsWidget ())
        else:
            self.messageOverlay = self.createMessageOverlay()
            self.formatOverlay()
            self.messageOverlay.opacity = 0.8
            mainWidget.setParentItem(self.messageOverlay)
            l = QGraphicsLinearLayout(self.messageOverlay)
            l.addItem(mainWidget)

        if self.messageDialog:
            pos = self.geometry().topLeft().toPoint()
            if (corona):
                pos = corona.popupPosition(self.applet, self.messageDialog.size())

            self.messageDialog.move(pos)
            #self.locationToDirection(self.location())
            self.messageDialog.animatedShow(Plasma.Direction(0))
            self.hidePopup()
        else:
            self.messageOverlay.show()

    def createMessageOverlay(self):
        if self.messageOverlay == None:
            messageOverlay = QGraphicsWidget(self.widget)
            return messageOverlay

    def formatOverlay(self):
        self.messageOverlay.resize(self.widget.contentsRect().size())
        self.messageOverlay.setPos(self.widget.contentsRect().topLeft())

        zValue = 100
        for child in  self.widget.children():
            if (child.zValue() > zValue):
                zValue = child.zValue() + 1
        self.messageOverlay.setZValue(zValue)

    def destroyMessageOverlay(self):
        if self.messageDialog != None:
            #Plasma::locationToInverseDirection(q->location())
            self.messageDialog.animatedHide(Plasma.Direction(0))
            self.messageDialog.deleteLater()
            self.messageDialog.hide()
            self.messageDialog = None
            self.showPopup(0)

        if self.messageOverlay == None:
            return

        self.messageOverlay.hide()
        self.messageOverlay = None

def CreateApplet(parent):
    # Veromix is dedicated to my girlfriend Vero.
    return VeroMixPlasmoid(parent)
