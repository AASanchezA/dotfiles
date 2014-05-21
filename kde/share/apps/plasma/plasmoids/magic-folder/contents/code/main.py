# -*- coding: utf-8 -*-
#
#   Copyright (C) 2009, 2010 Benjamin Kleiner <bizzl@user.sourceforge.net>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License version 2,
#   or (at your option) any later version, as published by the Free
#   Software Foundation
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the
#   Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdecore import i18n as _
from PyKDE4.kdeui import *
from PyKDE4.kio import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from configuration import FilterEditor, DisplayEditor
import os, re, PyKDE4.kdecore as kdecore

PANELS = [Plasma.Containment.CustomPanelContainment, Plasma.Containment.PanelContainment]

class MagicFolderApplet(plasmascript.Applet):
	def __init__(self, parent, args = None):
		plasmascript.Applet.__init__(self, parent)

	def init(self):
		if QFile(self.package().path() + "contents/locale/en/LC_MESSAGES/magic-folder.mo").exists() == False:
			proc = QProcess()
			proc.setProcessChannelMode(QProcess.MergedChannels)
			proc.start("bash", QStringList(self.package().path() + "contents/locale/compile.sh") )
			proc.waitForStarted()
			proc.waitForFinished()
			print proc.readAllStandardOutput()
		if (kdecore.versionMajor() == 4) and (kdecore.versionMinor() == 2) and (kdecore.versionRelease() < 90):
			translationPath = self.package().filePath("translations")
			if translationPath.isEmpty():
				translationPath = self.package().path() + "contents/locale/"
			KGlobal.dirs().addResourceDir("locale", translationPath)
			KGlobal.locale().insertCatalog( self.package().metadata().pluginName() )
		self.setHasConfigurationInterface(True)
		self.setLayout( QGraphicsLinearLayout(Qt.Vertical) )
		self.setContentsMargins(0, 0, 0, 0)
		self.layout().setContentsMargins(0, 0, 0, 0)
		self.setAcceptDrops(True)
		self.setAspectRatioMode(Plasma.Square)

		self.externalConfigFileName = KStandardDirs.locateLocal("config", "plasma_applet_magic_folderrc").__str__()
		self.extConfig = KConfig(self.externalConfigFileName)
		KMessageBox.setDontShowAskAgainConfig(self.extConfig)

		self.entries = []
		gc = self.config()
		self.iconUrl = gc.readEntry("icon", QVariant("folder-green") ).toString()
		self.labelString = gc.readEntry("label", QVariant(_("Magic Folder") ) ).toString()
		(count, bummer) = gc.readEntry("count", QVariant(-1) ).toInt()
		if count > 0:
			default = QStringList("*")
			default.append( os.path.expanduser("~") )
			default.append("True")
			default.append("False")
			for i in range(0, count):
				lst = gc.readXdgListEntry("_" + str(i), default)
				lst.append("")
				entry = {}
				entry["isWildcard"] = True
				if lst[2] == "False":
					entry["isWildcard"] = False
				entry["CaseSensitive"] = False
				if lst[3] == "True":
					entry["CaseSensitive"] = True
				entry["RegExp"] = lst[0]
				entry["Destination"] = lst[1]
				entry["isScript"] = False
				entry["justCopy"] = False
				self.entries.append(entry)
				gc.deleteEntry( "_" + str(i) )
			gc.deleteEntry("count")
			self.saveFilters()
		elif count == 0:
			gc.deleteEntry("count")
		else:
			self.loadFilters()
		self.icon = Plasma.IconWidget(KIcon(self.iconUrl), "", self.applet)
		self.connect(self.icon, SIGNAL("clicked()"), self.showConfigurationInterface)
		self.layout().addItem(self.icon)
		self.label = Plasma.Label()
		self.label.setText(self.labelString)
		self.label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
		if bool(self.labelString) and self.containment().containmentType() not in PANELS:
			self.layout().addItem(self.label)
			self.label.setVisible(True)

		self.connect(self, SIGNAL("saveState(KConfigGroup&)"), self.saveState)

	def saveFilters(self):
		counter = 0
		fc = self.extConfig.group("filters")
		fc.writeEntry("count", QVariant( len(self.entries) ) )
		for entry in self.entries:
			cc = fc.group("_" + str(counter) )
			cc.writeEntry("isWildcard", QVariant( entry["isWildcard"]) )
			cc.writeEntry("CaseSensitive", QVariant(entry["CaseSensitive"]) )
			cc.writeEntry("isScript", QVariant(entry["isScript"]) )
			cc.writeEntry("RegExp", QVariant(entry["RegExp"]) )
			cc.writeEntry("Destination", QVariant(entry["Destination"]) )
			cc.writeEntry("justCopy", QVariant(entry["justCopy"]) )
			counter += 1
		self.extConfig.sync()

	def loadFilters(self):
		fc = self.extConfig.group("filters")
		(count, bummer) = fc.readEntry("count", QVariant(0) ).toInt()
		if count > 0:
			for i in range(0, count):
				cc = fc.group("_" + str(i) )
				entry = {}
				entry["CaseSensitive"] = cc.readEntry("CaseSensitive", QVariant(False) ).toBool()
				entry["isWildcard"] = cc.readEntry("isWildcard", QVariant(True) ).toBool()
				entry["isScript"] = cc.readEntry("isScript", QVariant(False) ).toBool()
				entry["RegExp"] = cc.readEntry("RegExp", QVariant("*") ).toString().__str__()
				entry["Destination"] = cc.readEntry("Destination", QVariant( os.path.expanduser("~") ) ).toString().__str__()
				entry["justCopy"] = cc.readEntry("justCopy", QVariant(False) ).toString().__str__()
				self.entries.append(entry)

	@pyqtSignature("KConfigGroup&")
	def saveState(self, configGroup):
		self.saveFilters()
		configGroup.writeEntry("icon", QVariant(self.iconUrl) )
		configGroup.writeEntry("label", QVariant(self.labelString) )
		self.icon.setIcon(self.iconUrl)
		self.label.setText(self.labelString)
		if bool(self.labelString) and self.containment().containmentType() not in PANELS:
			self.layout().addItem(self.label)
			self.label.setVisible(True)
		else:
			self.layout().removeItem(self.label)
			self.label.setVisible(False)

	def contextualActions(self):
		return []

	def paintInterface(self, painter, option, rect):
		pass

	def constraintsEvent(self, constraints):
		if constraints & Plasma.FormFactorConstraint:
			self.setBackgroundHints(Plasma.Applet.NoBackground)

	def createConfigurationInterface(self, parent):
		self.filterEditor = FilterEditor(self.entries, self.package().path() )
		p = parent.addPage(self.filterEditor, _("Rules") )
		p.setIcon( KIcon("view-filter") )

		self.displayEditor = DisplayEditor(self.iconUrl, self.labelString)
		p = parent.addPage(self.displayEditor, _("Display") )
		p.setIcon( KIcon("preferences-desktop-display") )

		self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
		self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)
		pass

	def showConfigurationInterface(self):
		dialog = KPageDialog()
		dialog.setFaceType(KPageDialog.List)
		dialog.setButtons( KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel) )
		self.createConfigurationInterface(dialog)
		dialog.resize(500,400)
		dialog.exec_()

	def configAccepted(self):
		self.entries = self.filterEditor.exportList()
		self.iconUrl = self.displayEditor.icon()
		self.labelString = self.displayEditor.label()
		gc = self.config()
		self.saveState(gc)
		self.configDenied()

	def configDenied(self):
		self.filterEditor.deleteLater()
		self.displayEditor.deleteLater()

	def shouldConserveResources(self):
		return True

	def dragEnterEvent(self, e):
		e.accept()

	def filter(self, qlist, regexp):
		result = QStringList()
		for i in range(qlist.count() - 1, -1, -1):
			if not qlist[i].contains(regexp):
				result.append(qlist[i])
		return result

	# http://www.tuxfiles.org/linuxhelp/wildcards.html
	def wildcardCompiler(self, matchObj):
		if matchObj.group(0) == "*":
			return ".*"
		elif matchObj.group(0) == "?":
			return "."
		elif matchObj.group(0) == ".":
			return "\."
		elif matchObj.group(0) == "[!":
			return "[^"
		elif matchObj.group(0) == " ":
			return "|"
		else:
			return "(" + re.sub(",", "|", matchObj.group(1) ) + ")"

	def dropEvent(self, e):
		t = QStringList()
		for f in e.mimeData().urls():
			t << f.toString()
		self.sort(t)

	def filterList(self, l, regex):
		result = QStringList()
		for a in l:
			base = a.section(os.sep, -1)
			if regex.indexIn(base) >= 0:
				result << a
		return result

	def sort(self, t):
		# Note: atm we can't access anything from imap or mbox mailboxes
		mailboxes = t.filter(QRegExp("^(mailbox|mbox|imaps?):/"))
		for entry in mailboxes:
			t.removeAll(entry)
		if t.isEmpty():
			return
		i = t.count() - 1
		while i > -1:
			job = KIO.stat(KUrl(t[i]))
			job.exec_()
			result = job.statResult()
			if result.count() == 0:
				t.removeAt(i)
			i -= 1

		for entry in self.entries:
			if t.count() == 0:
				break
			format = QRegExp.RegExp2
			regexString = entry["RegExp"]
			if entry["isWildcard"]:
				#print regexString
				tmp = re.sub("\{([^}]+?)\}|\*|\.|\[!| |\?", self.wildcardCompiler, regexString)
				tmp = re.sub("[|]+", "|", tmp)
				regexString = "^(" + tmp + ")$"
				#print regexString
			case = Qt.CaseInsensitive
			if entry["CaseSensitive"]:
				case = Qt.CaseSensitive
			regex = QRegExp(regexString, case, format)
			if not regex.isValid():
				print "Error: Regular expression \"" + regexString + "\" is invalid!"
				continue
			dest = entry["Destination"]
			items = self.filterList(t, regex)
			if items.count() > 0:
				t = self.filter(t, regex)
				for f in items:
					print f.__str__().encode("latin-1")
				if not entry["isScript"]:
					if entry["justCopy"] == True:
						KIO.copy(KUrl.List(items), KUrl(dest) )
					else:
						KIO.move(KUrl.List(items), KUrl(dest) )
				else:
					for item in items:
						item = item.replace(QRegExp("^file:/"), "")
						proc = QProcess()
						proc.start(dest, QStringList(item) )
						proc.waitForStarted()
						proc.waitForFinished()
						response = QString( proc.readAllStandardOutput() ).replace(QRegExp("\n+$"), "")
						if not response.isEmpty():
							self.sort( response.split("\n") )
						print proc.readAllStandardError()



def CreateApplet(parent):
	return MagicFolderApplet(parent)

