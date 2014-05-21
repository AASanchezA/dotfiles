/****************************************************************************
**
** Copyright (C) 2012 Mike "rysiek" Woźniak <rysiek@hackerspace.pl>
** All rights reserved.
**
** GNU Lesser General Public License Usage
** This file may be used under the terms of the GNU Lesser General Public
** License version 2.1 as published by the Free Software Foundation and
** appearing in the file LICENSE.LGPL included in the packaging of this
** file. Please review the following information to ensure the GNU Lesser
** General Public License version 2.1 requirements will be met:
** http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU General
** Public License version 3.0 as published by the Free Software Foundation
** and appearing in the file LICENSE.GPL included in the packaging of this
** file. Please review the following information to ensure the GNU General
** Public License version 3.0 requirements will be met:
** http://www.gnu.org/copyleft/gpl.html.
**
****************************************************************************/

import QtQuick 1.1
import org.kde.plasma.core 0.1 as PlasmaCore

// editor of the item text
Rectangle {
  id: itiContainer
  anchors.fill: parent
  radius:2
  color: plasmaTheme.backgroundColor
  border {
    width:1
    color:plasmaTheme.highlightColor
  }
  visible: false

  // the text after editing
  property string text

  // handling visibility
  onVisibleChanged: {
    itiContainer.focus = true
  }

  // handling focus properly
  onFocusChanged: {
    if (focus == true) {
      itiInput.focus = true
      itiInput.selectAll()
    }
  }

  // plasma theme
  PlasmaCore.Theme {
    id: plasmaTheme
  }

  // mouse clicks handler
  MouseArea {
    anchors.fill: parent
    onClicked: { itiInput.focus = true }
  }

  // the text input
  TextInput {
    id: itiInput
    anchors {
      verticalCenter: parent.verticalCenter
      left: parent.left
      right: parent.right
      leftMargin: 3
      rightMargin: 3
    }
    horizontalAlignment: TextInput.AlignLeft
    text: itiContainer.text
    color: plasmaTheme.textColor
    onAccepted: {
      itiContainer.text = text
      itiContainer.visible = false
    }
    selectByMouse: true
    // handling the Escape key
    Keys.onEscapePressed: {
      itiContainer.visible = false
      text = itiContainer.text
    }
  }
}