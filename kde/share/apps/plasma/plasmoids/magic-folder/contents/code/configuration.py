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
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdecore import i18n as _
from PyKDE4.kdeui import *
from PyKDE4.kio import *

class FilterEditor(QWidget):
	def __init__(self, entries = None, selfPath = ""):
		QWidget.__init__(self)
		if entries == None:
			entries = []

		self.selfPath = selfPath

		# Pretty much the stuff you would get from pyuic for editor.ui
		self.verticalLayout = QVBoxLayout(self)

		self.wdtButtons = QToolBar(self)
		self.btnNew = QToolButton(self.wdtButtons)
		self.btnNew.setIcon( KIcon("document-new") )
		self.btnNew.setPopupMode(QToolButton.MenuButtonPopup)
		self.btnNewMenu = QMenu(self)
		self.btnNewMenu.addAction(KIcon("video-x-generic"), _("Video Files"), self, SLOT("videoClicked(bool)"))
		self.btnNewMenu.addAction(KIcon("image-x-generic"), _("Image Files"), self, SLOT("imageClicked(bool)"))
		self.btnNewMenu.addAction(KIcon("audio-x-generic"), _("Audio Files"), self, SLOT("audioClicked(bool)"))
		self.btnNewMenu.addAction(KIcon("text-x-generic"), _("Text Files"), self, SLOT("textClicked(bool)"))
		self.btnNewMenu.addAction(KIcon("application-x-zerosize"), _("Anything"), self, SLOT("newClicked(bool)"))
		self.btnNew.setMenu(self.btnNewMenu)
		self.wdtButtons.addWidget(self.btnNew)

		self.btnDelete = QToolButton(self.wdtButtons)
		self.btnDelete.setIcon( KIcon("edit-delete") )
		self.btnDelete.setEnabled(False)
		self.wdtButtons.addWidget(self.btnDelete)

		self.btnUp = QToolButton(self.wdtButtons)
		self.btnUp.setIcon( KIcon("arrow-up") )
		self.btnUp.setEnabled(False)
		self.wdtButtons.addWidget(self.btnUp)

		self.btnDown = QToolButton(self.wdtButtons)
		self.btnDown.setIcon( KIcon("arrow-down") )
		self.btnDown.setEnabled(False)
		self.wdtButtons.addWidget(self.btnDown)

		self.btnExport = QToolButton(self.wdtButtons)
		self.btnExport.setIcon( KIcon("document-export") )
		self.wdtButtons.addWidget(self.btnExport)

		self.btnImport = QToolButton(self.wdtButtons)
		self.btnImport.setIcon( KIcon("document-import") )
		self.wdtButtons.addWidget(self.btnImport)

		self.verticalLayout.addWidget(self.wdtButtons)

		self.lstMain = QListWidget(self)
		self.verticalLayout.addWidget(self.lstMain)

		self.widget = QWidget(self)
		sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
		self.widget.setSizePolicy(sizePolicy)
		self.formLayout = QFormLayout(self.widget)

		self.lblRegex = QLabel(self.widget)
		self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblRegex)
		self.edtRegex = QLineEdit(self.widget)
		self.formLayout.setWidget(1, QFormLayout.FieldRole, self.edtRegex)
		self.lblRegex.setBuddy(self.edtRegex)

		self.lblDestiny = QLabel(self.widget)
		self.formLayout.setWidget(5, QFormLayout.LabelRole, self.lblDestiny)
		self.edtDestiny = KUrlRequester(self.widget)
		self.edtDestiny.fileDialog().setMode(KFile.Directory)
		self.formLayout.setWidget(5, QFormLayout.FieldRole, self.edtDestiny)
		self.lblDestiny.setBuddy(self.edtDestiny)

		self.chbIsWildcard = QCheckBox(self.widget)
		self.formLayout.setWidget(2, QFormLayout.FieldRole, self.chbIsWildcard)

		self.chbIsCaseSensitive = QCheckBox(self.widget)
		self.formLayout.setWidget(3, QFormLayout.FieldRole, self.chbIsCaseSensitive)

		self.chbIsScript = QCheckBox(self.widget)
		self.btnScriptInfo = QPushButton(self.widget)
		self.btnScriptInfo.setIcon( KIcon("help-browser") )
		self.scriptLayout = QWidget(self.widget)
		QHBoxLayout(self.scriptLayout)
		self.scriptLayout.layout().setMargin(0)
		self.scriptLayout.layout().addWidget(self.chbIsScript)
		self.scriptLayout.layout().addWidget(self.btnScriptInfo)
		self.formLayout.setWidget(6, QFormLayout.FieldRole, self.scriptLayout)

		self.chbJustCopy = QCheckBox(self.widget)
		self.formLayout.setWidget(4, QFormLayout.FieldRole, self.chbJustCopy)

		self.verticalLayout.addWidget(self.widget)

		self.retranslateUi()

		for a in entries:
			item = QListWidgetItem( a["RegExp"] + ": " + a["Destination"] )
			item.setData(32, QVariant(a["RegExp"]) )
			item.setData(33, QVariant(a["Destination"]) )
			item.setData(34, QVariant(a["isWildcard"]) )
			item.setData(35, QVariant(a["CaseSensitive"]) )
			item.setData(36, QVariant(a["isScript"]) )
			item.setData(37, QVariant(a["justCopy"]) )
			self.lstMain.addItem(item)

		self.connect(self.edtDestiny, SIGNAL("textChanged(QString)"), self.destinyChanged)
		self.connect(self.edtRegex, SIGNAL("textChanged(QString)"), self.regexChanged)
		self.connect(self.lstMain, SIGNAL("itemSelectionChanged()"), self.selectionChanged)
		self.connect(self.chbIsWildcard, SIGNAL("stateChanged(int)"), self.checkboxStateChanged)
		self.connect(self.chbIsCaseSensitive, SIGNAL("stateChanged(int)"), self.checkboxStateChanged)
		self.connect(self.chbIsScript, SIGNAL("stateChanged(int)"), self.isScriptStateChanged)
		self.connect(self.chbIsScript, SIGNAL("stateChanged(int)"), self.checkboxStateChanged)
		self.connect(self.chbJustCopy, SIGNAL("stateChanged(int)"), self.checkboxStateChanged)
		self.connect(self.btnDelete, SIGNAL("clicked(bool)"), self.deleteClicked)
		self.connect(self.btnUp, SIGNAL("clicked(bool)"), self.upClicked)
		self.connect(self.btnDown, SIGNAL("clicked(bool)"), self.downClicked)
		self.connect(self.btnNew, SIGNAL("clicked(bool)"), self.newClicked)
		self.connect(self.btnExport, SIGNAL("clicked(bool)"), self.exportClicked)
		self.connect(self.btnImport, SIGNAL("clicked(bool)"), self.importClicked)
		self.connect(self.btnScriptInfo, SIGNAL("clicked(bool)"), self.scriptInfoClicked)

		self.changingFlag = False

	@pyqtSignature("bool")
	def scriptInfoClicked(self, b):
		if QDir( self.selfPath + "contents/help/" + KGlobal.locale().language() ).exists():
			url = KUrl(self.selfPath + "contents/help/" + KGlobal.locale().language() + "/script.html")
		else:
			url = KUrl(self.selfPath + "contents/help/script.html")
		KRun.runUrl(url, "text/html", self)


	@pyqtSignature("bool")
	def importClicked(self, b):
		filename = KFileDialog.getOpenFileName()
		if not filename.isEmpty():
			importConfig = KConfig(filename)
			fc = importConfig.group("filters")
			(count, bummer) = fc.readEntry("count", QVariant(0) ).toInt()
			if count > 0:
				for i in range(0, count):
					cc = fc.group("_" + str(i) )
					self.lstMain.addItem(" ")
					item = self.lstMain.item(self.lstMain.count() - 1)
					item.setData(32, cc.readEntry("RegExp", QVariant("*") ) )
					item.setData(33, cc.readEntry("Destination", QVariant( os.path.expanduser("~") ) ) )
					item.setData(34, cc.readEntry("isWildcard", QVariant(True) ) )
					item.setData(35, cc.readEntry("CaseSensitive", QVariant(False) ) )
					item.setData(36, cc.readEntry("isScript", QVariant(False) ) )
					item.setData(37, cc.readEntry("justCopy", QVariant(False) ) )
					a = item.data(32).toString()
					b = item.data(33).toString()
					item.setText(a + ": " + b)

	@pyqtSignature("bool")
	def exportClicked(self, b):
		filename = KFileDialog.getSaveFileName()
		if not filename.isEmpty():
			exportConfig = KConfig(filename)
			fc = exportConfig.group("filters")
			fc.writeEntry("count", QVariant( self.lstMain.count() ) )
			for i in range(0, self.lstMain.count() ):
				cc = fc.group("_" + str(i) )
				item = self.lstMain.item(i)
				fc.writeEntry("RegExp", item.data(32) )
				fc.writeEntry("Destination", item.data(33) )
				fc.writeEntry("isWildcard", item.data(34) )
				fc.writeEntry("CaseSensitive", item.data(35) )
				fc.writeEntry("isScript", item.data(36) )
				fc.writeEntry("justCopy", item.data(37) )

	@pyqtSignature("bool")
	def imageClicked(self, b):
		offers = KMimeType.allMimeTypes()
		result = QStringList()
		for a in offers:
			if a.name().contains( QRegExp("^image/") ):
				result << a.patterns().join(" ")
		self.newClicked( result.join(" ").__str__()  )

	@pyqtSignature("bool")
	def audioClicked(self, b):
		offers = KMimeType.allMimeTypes()
		result = QStringList()
		for a in offers:
			if a.name().contains( QRegExp("^audio/") ):
				result << a.patterns().join(" ")
		self.newClicked( result.join(" ").__str__()  )

	@pyqtSignature("bool")
	def videoClicked(self, b):
		offers = KMimeType.allMimeTypes()
		result = QStringList()
		for a in offers:
			if a.name().contains( QRegExp("^video/") ):
				result << a.patterns().join(" ")
		self.newClicked( result.join(" ").__str__()  )


	@pyqtSignature("bool")
	def textClicked(self, b):
		offers = KMimeType.allMimeTypes()
		result = QStringList()
		for a in offers:
			if a.name().contains( QRegExp("^text/") ):
				result << a.patterns().join(" ")
		self.newClicked( result.join(" ").__str__()  )

	@pyqtSignature("bool")
	def newClicked(self, b):
		regex = "*"
		if type(b) != bool:
			regex = b
		self.lstMain.addItem(regex + ": " + os.path.expanduser("~") )
		item = self.lstMain.item(self.lstMain.count() - 1)
		item.setData(32, QVariant(regex) )			# RegExp
		item.setData(33, QVariant( os.path.expanduser("~") ) )	# Destination
		item.setData(34, QVariant(True) )			# isWildcard
		item.setData(35, QVariant(False) )			# CaseSensitive
		item.setData(36, QVariant(False) )			# isScript
		item.setData(37, QVariant(False) )			# justCopy
		self.lstMain.setCurrentItem(item)

	@pyqtSignature("bool")
	def upClicked(self, b):
		row = self.lstMain.currentRow()
		item = self.lstMain.takeItem(row)
		self.lstMain.insertItem(row - 1, item)
		self.lstMain.setCurrentItem(item)

	@pyqtSignature("bool")
	def downClicked(self, b):
		row = self.lstMain.currentRow()
		item = self.lstMain.takeItem(row)
		self.lstMain.insertItem(row + 1, item)
		self.lstMain.setCurrentItem(item)

	@pyqtSignature("bool")
	def deleteClicked(self, b):
		self.lstMain.takeItem( self.lstMain.currentRow() )
		if self.lstMain.count() == 0:
			self.btnDelete.setEnabled(False)
			self.btnDown.setEnabled(False)
			self.btnUp.setEnabled(False)

	def selectionChanged(self):
		if self.lstMain.currentItem() != None:
			self.changingFlag = True
			self.edtDestiny.lineEdit().setText( self.lstMain.currentItem().data(33).toString() )
			self.edtRegex.setText( self.lstMain.currentItem().data(32).toString() )
			self.chbIsWildcard.setChecked( self.lstMain.currentItem().data(34).toBool() )
			self.chbIsCaseSensitive.setChecked( self.lstMain.currentItem().data(35).toBool() )
			self.chbIsScript.setChecked( self.lstMain.currentItem().data(36).toBool() )
			self.chbJustCopy.setChecked( self.lstMain.currentItem().data(37).toBool() )
			self.btnDelete.setEnabled(True)
			self.btnUp.setEnabled(self.lstMain.currentRow() > 0)
			self.btnDown.setEnabled(self.lstMain.currentRow() < self.lstMain.count() - 1)
			self.changingFlag = False

	@pyqtSignature("int")
	def checkboxStateChanged(self, i):
		if not self.changingFlag and not self.lstMain.currentItem() == None:
			self.lstMain.currentItem().setData(34, QVariant(self.chbIsWildcard.checkState() == Qt.Checked) )
			self.lstMain.currentItem().setData(35, QVariant(self.chbIsCaseSensitive.checkState() == Qt.Checked) )
			self.lstMain.currentItem().setData(37, QVariant(self.chbJustCopy.checkState() == Qt.Checked) )
			self.lstMain.currentItem().setData(36, QVariant(self.chbIsScript.checkState() == Qt.Checked) )

	@pyqtSignature("int")
	def isScriptStateChanged(self, i):
		if i == Qt.Checked and not self.changingFlag:
			KMessageBox.information(self, _("Scripting is a relativly stiff feature, please press the button next to the checkbox to inform yourself further."), QString(), _("scripting") )

	@pyqtSignature("QString")
	def regexChanged(self, string):
		if not self.changingFlag and not self.lstMain.currentItem() == None:
			self.lstMain.currentItem().setData(32, QVariant(string) )
			self.updateList()

	@pyqtSignature("QString")
	def destinyChanged(self, url):
		if not self.changingFlag and not self.lstMain.currentItem() == None:
			self.lstMain.currentItem().setData(33, QVariant(url) )
			self.updateList()

	def updateList(self):
		a = self.lstMain.currentItem().data(32).toString()
		b = self.lstMain.currentItem().data(33).toString()
		self.lstMain.currentItem().setText(a + ": " + b)

	def retranslateUi(self):
		self.btnDelete.setToolTip( _("Delete") )
		self.btnNew.setToolTip( _("New") )
		self.btnUp.setToolTip( _("Up") )
		self.btnDown.setToolTip( _("Down") )
		self.btnExport.setToolTip( _("Export") )
		self.btnImport.setToolTip( _("Import") )
		self.btnScriptInfo.setToolTip( _("About Scripts...") )
		self.lblRegex.setText( _("Regex") )
		self.lblDestiny.setText( _("Destiny") )
		self.chbIsWildcard.setText( _("Wildcard") )
		self.chbIsCaseSensitive.setText( _("Case Sensitive") )
		self.chbIsScript.setText( _("Destiny is a Script") )
		self.chbJustCopy.setText( _("Copy Only") )

	def exportList(self):
		result = []
		for i in range(0, self.lstMain.count() ):
			entry = {}
			item = self.lstMain.item(i)
			entry["RegExp"] = item.data(32).toString().__str__()
			entry["Destination"] = item.data(33).toString().__str__()
			entry["isWildcard"] = item.data(34).toBool()
			entry["CaseSensitive"] = item.data(35).toBool()
			entry["isScript"] = item.data(36).toBool()
			entry["justCopy"] = item.data(37).toBool()
			result.append(entry)
		return result

class DisplayEditor(QWidget):
	def __init__(self, icon, string):
		QWidget.__init__(self)
		QFormLayout(self)
		self.layout().setLabelAlignment(Qt.AlignCenter)

		self.iconLabel = QLabel(self)
		self.layout().setWidget(0, QFormLayout.LabelRole, self.iconLabel)

		self.iconButton = KIconButton(self)
		self.iconButton.setIcon(icon)
		self.layout().setWidget(0, QFormLayout.FieldRole, self.iconButton)

		self.labelLabel = QLabel(self)
		self.layout().setWidget(1, QFormLayout.LabelRole, self.labelLabel)

		self.labelEditor = QLineEdit(self)
		self.labelEditor.setText(string)
		self.layout().setWidget(1, QFormLayout.FieldRole, self.labelEditor)

		self.retranslateUi()

	def retranslateUi(self):
		self.iconLabel.setText( _("Icon") )
		self.labelLabel.setText( _("Label") )

	def icon(self):
		return self.iconButton.icon().__str__()

	def label(self):
		return self.labelEditor.text().__str__()

