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

import QtQuick 1.0
import org.kde.plasma.core 0.1 as PlasmaCore

Rectangle {
  id: buttonShade
  anchors.fill: parent;
  radius: parent.radius;
  opacity: .4

  property string state: ""
  property color shadeColor: "black"
  property color hoverColor: "blue"
  color: "white"

  property variant gradientStops: [0, 0.57, 0.9]

  gradient: Gradient {
    id: theGradient
    GradientStop {id: g1; color: buttonShade.color; position: buttonShade.gradientStops[0]}
    GradientStop {id: g2; color: buttonShade.color; position: buttonShade.gradientStops[1]}
    GradientStop {id: g3; color: shadeColor; position: buttonShade.gradientStops[2]}
  }

  states: [
    State {
      name: "pressed"
      when: state == "pressed"
      PropertyChanges {
        target: g1
        color: hoverColor
      }
      PropertyChanges {
        target: g2
        color: buttonShade.color
      }
      PropertyChanges {
        target: g3
        color: buttonShade.color
      }
    },
    State {
      name: "hovered"
      when: state == "hovered"
      PropertyChanges {
        target: g1
        color: buttonShade.color
      }
      PropertyChanges {
        target: g2
        color: buttonShade.color
      }
      PropertyChanges {
        target: g3
        color: hoverColor
      }
    }
  ]
}