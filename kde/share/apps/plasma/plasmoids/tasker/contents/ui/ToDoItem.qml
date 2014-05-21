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

Rectangle {
  id: itemContainer

  // height is height of the area for items divided by visible item count
  height: Math.max(
    (mainContainer.height - mainCaption.height) / ( mainContainer.visibleItems + 1 ),
    32
  // plus the area for children plus the children area y coord (if children are visible)
  ) + ( (todosContainer.visible) ? ( todosContainer.childrenRect.height + todosContainer.childrenRect.y ) : 0 )
    
  color:"#00000000"
  opacity: { return (itemContainer.done) ? 0.6 : 1 }
  
  anchors {
    left: parent.left
    right: parent.right
  }

  // properties
  property int subItemsCount: 0
  property alias text: todoTextInputContainer.text
  property int elapsed: 0
  property alias running: itemTimer.running
  property alias editing: todoTextInputContainer.visible
  property bool done: false
  property alias expanded: collapser.toggled
  property Item oldparent: null
  property Column subitemContainer: todosContainer

  // is the item being dleted
  // (needed to distinguish between todo item user-delete and plasmoid destruction)
  property bool deleting: false
  
  Component.onCompleted: {
    // some basic data
    mainContainer.todoItems += 1
    text = '[task #' + mainContainer.todoItems + ']'
    editing = true
  }

  Component.onDestruction: {
    // bookkeeping
    mainContainer.todoItems -= 1
    // save task config *only* if the task is being deleted on user request
    // rather than because the plasmoid is being destroyed
    if (itemContainer.deleting == true) saveTaskConfig()
  }
  
  onDoneChanged: {
    // bookkeeping
    if (done == true) expanded = false
    running = false
    // saving the config
    saveTaskConfig()
  }

  onVisibleChanged: {
    //console.log(text + " visible changed: " + visible)
    if (visible) {
      mainContainer.hiddenItems -= 1
    } else {
      mainContainer.hiddenItems += 1
    }
  }

  onEditingChanged: {
    // inform
    //console.log('editing changed to: ' + editing)
    // after finishing the editing, save the config
    if (editing == false) saveTaskConfig()
  }

  onExpandedChanged: {
    // saving the config
    saveTaskConfig()
  }

  onRunningChanged: {
    // saving the config
    saveTaskConfig()
  }

  // plasma theme
  PlasmaCore.Theme {
    id: plasmaTheme
  }

  Timer {
    id: itemTimer
    repeat: true
    onTriggered: { itemContainer.elapsed += 1 }
  }
  
  Rectangle {
    id: itemParent
    anchors {
      fill: parent
      bottomMargin:2
      topMargin:2
    }
    border.width:1
    border.color: { return (itemContainer.done || itemContainer.running) ? "#006600" : "#660000" }
    radius: 4
    color:"#00000000"
  
    // the todo item itself
    Rectangle {
      id: item
      anchors {
        left: parent.left
        right: parent.right
        top: parent.top
      }
      radius: parent.radius
      color:"#00000000"
      height: Math.max(
        (mainContainer.height - mainCaption.height) / ( mainContainer.visibleItems + 1 ) - 4,
        28
      )

      MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        onClicked: { itemContainer.running = ! itemContainer.running }
        enabled: ! itemContainer.done
        drag.axis: Drag.YAxis
        drag.target: itemContainer
        // we want this MouseArea to handle drags, but the right children to handle clicks (i.e. MouseAreas in buttons)
        drag.filterChildren: true
        // handling the changed position
        onPositionChanged: {
          // first we need to de-parent the bugger
          if ( (drag.active == true) && (itemContainer.oldparent == null) ) {
            // getting the old y coord
            var coords = itemParent.mapToItem(mainContainer, itemParent.x, itemParent.y)
            // removing the acnhors
            itemParent.anchors.fill = undefined
            // off-setting the visible portion of the item so that it always appears under the mouse while dragged
            itemParent.y = coords.y - itemContainer.y
            // changing the parent
            //console.log('deparenting')
            //console.log("+- parent's children before : " + itemContainer.parent.children.length)
            itemContainer.oldparent = itemContainer.parent
            itemContainer.parent = mainContainer
            //console.log("+- parent's children after  : " + itemContainer.oldparent.children.length)
          }
        }
        onReleased: {
          if (drag.active == true) {
            // we do not want the "click" to propagate further(?)
            mouse.accepted = true
            var p = mainContainer.subitemContainer
            var lcol = p // last "column" type
            xy = mapToItem(p, mouse.x, mouse.y)
            while (np = p.childAt(xy.x, xy.y)) {
              //console.log("tried childAt(" + xy.x + ', ' + xy.y + "); got: " + np)
              p = np
              if (p.isColumn == true) lcol = p
              xy = mapToItem(p, mouse.x, mouse.y)
            }
            //console.log('dropped on: ' + p + ', attaching to: ' + lcol)
            itemContainer.parent = lcol
            itemContainer.oldparent = null
            // anchors
            itemParent.anchors.fill = itemContainer
            // saving the config
            saveTaskConfig()
          }
        }
      }

      states: [
        State {
          name: "pressed"
          when: ( mouseArea.pressed == true ) && ( mouseArea.drag.active == false )
          PropertyChanges {
            target: itemShade
            state: "pressed"
          }
          PropertyChanges {
            target: todoCaptionOuterContainer
            anchors.verticalCenterOffset: 0
            anchors.horizontalCenterOffset: 1
          }
        },
        State {
          name: "hovered"
          when: ( mouseArea.containsMouse == true ) && ( mouseArea.pressed == false )
          PropertyChanges {
            target: itemShade
            state: "hovered"
          }
          PropertyChanges {
            target:todoCaption
            state: "hovered"
          }
        },
        // dragging
        State {
          name: "dragged"
          when: ( mouseArea.pressed == true ) && ( mouseArea.drag.active == true )
          PropertyChanges {
            target: itemShade
            state: "pressed"
          }
          PropertyChanges {
            target: itemContainer
            opacity: 0.4
            z: 1
          }
        }
      ]

      // highlight
      HighlightShade {
        id: itemShade
        color: { return (itemContainer.done || itemContainer.running) ? "#66aa66" : "#aa6666" } // plasmaTheme.buttonBackgroundColor tinted?
        shadeColor:"#00000000"
        hoverColor: { return (itemContainer.done || itemContainer.running) ? "#006600" : "#660000" }
        opacity:0.8
      }
        
      // show/collapse button
      Button {
        id: collapser
        anchors {
          verticalCenter: parent.verticalCenter
          left:parent.left
          leftMargin:3
        }
        color: "#00000000"
        hoverColor: { return (itemContainer.done || itemContainer.running) ? "#008800" : "#880000" }
        width:12
        height:12
        opacity:.4
        hoverOpacity:.9
        pressedOpacity:1.0
        text: "☰" // { return (itemContainer.expanded) ? "↑" : "↓" }
        font.pixelSize: 10
        textVOffset: 0
        textHOffset: 0
        toggling: true
        toggled: true
      }

      Text {
        id: leftEllipsis
        text:"…"
        anchors {
          left: collapser.right
          top: parent.top
          bottom: parent.bottom
          leftMargin:3
        }
        clip:true
        horizontalAlignment: Text.AlignRight
        verticalAlignment: Text.AlignVCenter
        smooth: true
        color: plasmaTheme.textColor
        font.strikeout: itemContainer.done

        states: [
          State {
            name: "hidden"
            when: (todoCaption.width <= todoCaptionOuterContainer.width) || (todoCaption.state != "hovered")
            PropertyChanges {
              target: leftEllipsis
              width: 0
            }
          },
          State {
            name: "visible"
            when: (todoCaption.width > todoCaptionOuterContainer.width) && (todoCaption.state == "hovered")
            PropertyChanges {
              target: leftEllipsis
              width: leftEllipsis.implicitWidth
            }
          }
        ]

        transitions: Transition {
          NumberAnimation {
            properties: "width"
            easing.type: Easing.Linear
            duration: 200
          }
          reversible: true
        }
      }

      // todo text container, needed to be able to run the onhover animation
      Item {
        id: todoCaptionOuterContainer
        clip: true
        anchors {
          top: parent.top
          bottom: parent.bottom
          left:leftEllipsis.right
          right:rightEllipsis.left
        }

        // todo caption inner container for nicer scroll animation
        Item {
          id: todoCaptionInnerContainer
          clip: false
          // full
          anchors {
            top: parent.top
            bottom: parent.bottom
          }
          x: -1 * leftEllipsis.width

          // the todo text
          Text {
            id: todoCaption
            text: todoTextInputContainer.text
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            smooth: true
            wrapMode: Text.Wrap
            color: plasmaTheme.textColor
            font.strikeout: itemContainer.done
            anchors {
              top:parent.top
              bottom:parent.bottom
            }
            elide: Text.ElideNone
            clip: false
            maximumLineCount: 1

            states: [
              State {
                name: "hovered"
                PropertyChanges {
                  target: todoCaption
                  x: (todoCaption.width > todoCaptionOuterContainer.width) ? todoCaptionOuterContainer.width - todoCaption.width + rightEllipsis.implicitWidth : 0
                }
              }
            ]

            // handling state change
            // we need to handle aniation durations here as otherwise they get looped because of binding
            onStateChanged: {
              // animating to "hovered" state - if there is, in fact, what to animate, then make the duration dependant on both the total scroll needed and how far the text is already scrolled
              toAnimation.duration = (todoCaption.width > todoCaptionOuterContainer.width) ? (todoCaption.width - todoCaptionOuterContainer.width + todoCaption.x) * 10 : 0
              // animating from "hovered" state - if there is what to animate, then make the duration dependant on how far the text is already scrolled
              fromAnimation.duration = (todoCaption.width > todoCaptionOuterContainer.width) ? todoCaption.x * -10 : 0
            }

            transitions: [
              Transition {
                to: "hovered"
                NumberAnimation {
                  id: toAnimation
                  properties: "x"
                  easing.type: Easing.InOutSine
                }
              },
              Transition {
                from: "hovered"
                NumberAnimation {
                  id: fromAnimation
                  properties: "x"
                  easing.type: Easing.InOutSine
                }
              }
            ] // transitions

          } // todoCaption
        } // todoCaptionInnerContainer
      } // todoCaptionOuterContainer

      Text {
        id: rightEllipsis
        text:"…"
        anchors {
          right:todoTimeDisplay.left
          rightMargin:4
          top: parent.top
          bottom: parent.bottom
        }
        clip:true
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
        smooth: true
        color: plasmaTheme.textColor
        font.strikeout: itemContainer.done

        states: [
          State {
            name: "hidden"
            when: (todoCaption.width <= todoCaptionOuterContainer.width) || (todoCaption.state == "hovered")
            PropertyChanges {
              target: rightEllipsis
              width: 0
            }
          },
          State {
            name: "visible"
            when: (todoCaption.width > todoCaptionOuterContainer.width) && (todoCaption.state != "hovered")
            PropertyChanges {
              target: rightEllipsis
              width: rightEllipsis.implicitWidth
            }
          }
        ]

        transitions: Transition {
          NumberAnimation {
            properties: "width"
            easing.type: Easing.Linear
            duration: 200
          }
          reversible: true
        }
      }

      // timing
      Text {
        id: todoTimeDisplay
        text: {
          // get the data
          s = itemContainer.elapsed % 60
          m = Math.floor((itemContainer.elapsed % 3600) / 60)
          h = Math.floor(itemContainer.elapsed / 3600)
          // we'd like to have them double-digit, always
          if (s < 10) s = '0' + s
          if (m < 10) m = '0' + m
          if (h < 10) h = '0' + h
          // return the formatted string
          return "(" + h + ":" + m + ":" + s + ")"
        }
        horizontalAlignment: Text.AlignRight
        verticalAlignment: Text.AlignVCenter
        smooth: true
        font.italic: true
        wrapMode: Text.NoWrap
        color: plasmaTheme.textColor
        anchors {
          top: parent.top
          bottom: parent.bottom
          right:textEditButton.left
          rightMargin:3
        }
        font.strikeout: itemContainer.done
      }

      // toggle text edit field
      Button {
        id: textEditButton
        anchors {
          verticalCenter: parent.verticalCenter
          right:addSubItem.left
          rightMargin:3
        }
        color: "#00000000"
        hoverColor: { return (itemContainer.done || itemContainer.running) ? "#008800" : "#880000" }
        width:12
        height:12
        opacity:.4
        hoverOpacity:.9
        pressedOpacity:1.0
        onClicked: { itemContainer.editing = true }
        text:"⌶"
        font.pixelSize: 9
        textVOffset: 0
        textHOffset: 2
        toggling: false
        enabled: ! itemContainer.done
      }

      // add subitem button
      Button {
        id: addSubItem
        anchors {
          verticalCenter: parent.verticalCenter
          right:markDone.left
          rightMargin:3
        }
        color: "#00000000"
        hoverColor: { return (itemContainer.done || itemContainer.running) ? "#008800" : "#880000" }
        width:12
        height:12
        opacity:.4
        hoverOpacity:.9
        pressedOpacity:1.0
        disabledOpacity:0.2
        onClicked: {
          itemContainer.expanded = true
          addToDoItem(todosContainer)
        }
        text:"+"
        font.pixelSize: 10
        enabled: ! itemContainer.done
        textVOffset: 0
        textHOffset: 1
      }

      // toggle mark as done
      Button {
        id: markDone
        anchors {
          verticalCenter: parent.verticalCenter
          right:deleteItem.left
          rightMargin:3
        }
        color: "#00000000"
        hoverColor: { return (itemContainer.done || itemContainer.running) ? "#008800" : "#880000" }
        width:12
        height:12
        opacity:.4
        hoverOpacity:.9
        pressedOpacity:1.0
        onClicked: { itemContainer.done = ! itemContainer.done }
        text: { return (itemContainer.done) ? "✔" : "✓" }
        font.pixelSize: 10
        textVOffset: 0
        textHOffset: 1
        toggling: true
        toggled: false
      }

      // delete, with children!
      Button {
        id: deleteItem
        anchors {
          verticalCenter: parent.verticalCenter
          right:parent.right
          rightMargin:3
        }
        color: "#00000000"
        hoverColor: { return (itemContainer.done || itemContainer.running) ? "#008800" : "#880000" }
        width:12
        height:12
        opacity:.4
        hoverOpacity:.9
        pressedOpacity:1.0
        onClicked: {
          itemContainer.deleting = true
          itemContainer.destroy()
        }
        text:"×"
        font.pixelSize: 10
        textVOffset: 0
        textHOffset: 1
        toggling: false
        toggled: false
      }

      // editor of the item text
      ImprovedTextInput {
        id: todoTextInputContainer
        text: "[new item]"
      }
    }

    Column {
      id: todosContainer
      anchors {
        top: item.bottom
        topMargin:2
        bottom:parent.bottom
        bottomMargin: 2
        left: parent.left
        right: parent.right
        leftMargin:5
        rightMargin:2
      }
      visible: itemContainer.expanded
      property bool isColumn: true
    }


    /*PlasmaCore.ToolTip {
      target: item
      mainText: todoCaption.text + "<br/><em>" + todoTimeDisplay.text + "</em>"
      subText: "This Task has " + todosContainer.children.length + " sub-tasks"
    }*
    
    PlasmaCore.ToolTip {
      target: markDone
      mainText: "Mark as Done"
      subText: "Mark/unmark the given Task as done"
    }

    PlasmaCore.ToolTip {
      target: addSubItem
      mainText: "Add a Sub-Task"
      subText: "Add a sub-task to the given Task"
    }

    PlasmaCore.ToolTip {
      target: collapser
      mainText: "Collapse"
      subText: "Show/hide sub-tasks of the given Task"
    }/**/
  }
}