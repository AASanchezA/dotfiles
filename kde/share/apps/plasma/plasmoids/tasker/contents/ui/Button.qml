/****************************************************************************
**
** Copyright (C) 2012 Mike "rysiek" Woźniak <rysiek@hackerspace.pl>
** All rights reserved.
**
** This file is based on part of the QtDeclarative module of the Qt Toolkit
** by Nokia Corporation <qt-info@nokia.com>
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

import QtQuick 1.0

Rectangle {
  id: button

  property alias text: buttonText.text
  property alias textColor: buttonText.color
  property alias enabled: mouseArea.enabled
  property alias font: buttonText.font
  property color hoverColor: "green"
  property color shadeColor: "black"
  property real hoverOpacity: 1.0
  property real pressedOpacity: 1.0
  property real disabledOpacity: 0.4
  property bool toggling: false
  property bool toggled: false
  property int textVOffset: -1
  property int textHOffset: 0
  color: "white"

  signal clicked

  smooth: true
  radius: 2
  border.color: button.hoverColor // binding does not work here, wtf?
  border.width: 1

  onTogglingChanged: {
    if (! toggling) button.toggled = false
    console.log('Toggling changed to ' + toggling)
  }
  
  onToggledChanged: {
    console.log('toggled changed to ' + toggled)
  }
  
  HighlightShade {
    id: buttonShade
    color: parent.color
    shadeColor: parent.shadeColor
    hoverColor: parent.hoverColor
  }

  Text {
    id: buttonText
    anchors.centerIn: parent
    anchors.verticalCenterOffset: button.textVOffset
    anchors.horizontalCenterOffset: button.textHOffset
    font.pixelSize: parent.width > parent.height ? parent.height * .4 : parent.width * .4
    smooth: true
    text: "black"
  }

  MouseArea {
    id: mouseArea
    anchors.fill: parent
    hoverEnabled: true
    onClicked: {
      if (button.toggling) button.toggled = ! button.toggled
      button.clicked()
    }
  }

  states: [
    State {
      name: "disabled"
      when: enabled == false
      PropertyChanges {
        target: button
        opacity: disabledOpacity
      }
    },
    State {
      name: "pressed"
      when: ( mouseArea.pressed == true ) || ( ( button.toggling == true ) && ( button.toggled == true ) )
      PropertyChanges {
        target: buttonShade
        state: "pressed"
      }
      PropertyChanges {
        target: buttonText
        anchors.verticalCenterOffset: button.textVOffset + 1
        anchors.horizontalCenterOffset: button.textHOffset + 1
      }
      PropertyChanges {
        target: button
        opacity: pressedOpacity
      }
    },
    State {
      name: "hovered"
      when: ( mouseArea.containsMouse == true ) && ( mouseArea.pressed == false )
      PropertyChanges {
        target: buttonShade
        state: "hovered"
      }
      PropertyChanges{
        target: button
        opacity: hoverOpacity
      }
    }
  ]
}