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
import org.kde.plasma.components 0.1 as PlasmaComponents

Item {
  id: outerContainer

  // minimum dimensions
  property int minimumWidth: 256
  property int minimumHeight: 64

  // reading config flag
  property bool readingConfig: false
  
  Component.onCompleted: {
    // context-menu
    // plasmoid.setAction(String name, String text, String icon, String shortcut))
    plasmoid.action_labelEdit = function() {
      mainCaption.editing = ! mainCaption.editing
    }
    plasmoid.setAction('labelEdit', i18n('Edit label'))
    // config
    plasmoid.activeConfig = "main";
    mainCaption.configuredText = plasmoid.readConfig("TaskerLabel")
    // loading the items
    print('Just Added: ' + plasmoid.readConfig("JustAdded"))
    loadToDoItem(plasmoid.readConfig("JustAdded"))
    plasmoid.writeConfig("JustAdded", false);
  }

  // loading the ToDoItem definition
  function loadToDoItem(just_added) {
    // load the todo item definition
    mainContainer.todoItemComponent = Qt.createComponent("ToDoItem.qml");
    // are we ready?
    if (mainContainer.todoItemComponent.status == Component.Ready) {
      // should we actually add an empty item?
      if (just_added == true) {
        var tdi = mainContainer.todoItemComponent.createObject(todosContainer);
      // nope. apparently we should try loading the tasks config!
      } else {
        readTaskConfig()
      }
    } else {
      console.log('ERROR: ' + mainContainer.todoItemComponent.errorString())
    }
  }

  // adding a todo item
  function addToDoItem(cnt) {
    // create the object
    var tdi = mainContainer.todoItemComponent.createObject(cnt)
    // save the config - this routine checks on its own if we're during config reading
    saveTaskConfig()
    // return the created object for further processing
    return tdi
  }

  // getting all relevant task data as JSON
  function getTaskJSON(cnt) {
    // container array
    var tasks = []
    // default cnt
    if (cnt == undefined) {
      //console.log('getTaskJSON() : cnt undefined, using default (mainContainer)')
      cnt = mainContainer
    }
    // iterate through items
    //console.log('getTaskJSON() : ' + cnt.objectName + ' : iterating through ' + cnt.subitemContainer.children.length + ' items')
    for (var t=0; t<cnt.subitemContainer.children.length; t++) {
      // if the item is being deleted, pass it over (along with its children)
      if (cnt.subitemContainer.children[t].deleting) continue
      // work on the item, get the data
      with (cnt.subitemContainer.children[t]) {
        // basic data
        var td = {
          text: text,
          elapsed: elapsed,
          running: running,
          done: done,
          expanded: expanded,
          subitems: []
        }
      }
      // subitems
      td.subitems = getTaskJSON(cnt.subitemContainer.children[t])
      // get it to the tasks array
      tasks.push(td)
      //console.log('getTaskJSON() : ' + cnt.objectName + ' : ' + t)
    }
    //console.log('getTaskJSON() : ' + cnt.objectName + ' : ' + JSON.stringify(tasks))
    // return whatever we got
    return tasks
  }

  // saving task config
  function saveTaskConfig() {
    // check the flag
    if (outerContainer.readingConfig == true) return false
    // inform
    //console.log('saving task config...')
    // write to config
    plasmoid.writeConfig(
      "Items",
      // stringify the task info
      JSON.stringify(
        getTaskJSON()
      )
    );
    //console.log('saving task config... done')
  }


  // removing all tasks
  function removeAllTasks() {
    for (var t=0; t<mainContainer.subitemContainer.children.length; t++) {
      mainContainer.subitemContainer.children[t].destroy()
    }
  }


  // create task from config
  function createTaskFromConfig(tasks, cnt) {
    // default cnt
    if (cnt == undefined) {
      //console.log('createTaskFromConfig() : cnt undefined, using default (mainContainer)')
      cnt = mainContainer
    }
    // create task items
    for (var t in tasks) {
      // info
      //console.log('createTaskFromConfig() : working with: ' + tasks[t].text)
      // create it - informing that "yes, it is created from config"
      var obj = addToDoItem(cnt.subitemContainer)
      // set the properties
      obj.text = tasks[t].text
      obj.elapsed = tasks[t].elapsed
      obj.running = tasks[t].running
      obj.done = tasks[t].done
      obj.expanded = tasks[t].expanded
      obj.editing = false
      // create subtasks
      createTaskFromConfig(tasks[t].subitems, obj)
    }
  }

  // reading items from task config
  function readTaskConfig() {
    // inform
    //console.log('readTaskConfig() : reading task config...')
    // set the flag
    outerContainer.readingConfig = true
    // get the config data
    var tasks = []
    try {
       tasks = JSON.parse(plasmoid.readConfig("Items"))
    } catch (e) {
      console.log('readTaskConfig() : error retrieving task config: ' + e)
    }
    //console.log('readTaskConfig() : got config: ' + JSON.stringify(tasks))
    // remove all tasks
    removeAllTasks()
    // create tasks
    createTaskFromConfig(tasks)
    // unset the flag
    outerContainer.readingConfig = false
  }

  // plasma theme, needed for styling
  PlasmaCore.Theme {
    id: plasmaTheme
  }

  // the scrollbar
  PlasmaComponents.ScrollBar {
    id: mainScroll
    flickableItem: mainContainer
    anchors {
      right:parent.right
    }
  }

  // main container for all our needs
  Flickable {
    id: mainContainer

    // size
    anchors {
      fill: parent
      rightMargin: mainScroll.visible ? mainScroll.width : 0
    }
    
    // properties
    property int todoItems: 0
    property int hiddenItems: 0
    property int visibleItems: todoItems - hiddenItems
    property Component todoItemComponent: null
    property Column subitemContainer: todosContainer

    // needed for the flickable part
    clip: true
    contentWidth: width
    contentHeight: mainCaption.height + todosContainer.childrenRect.height + globalAddToDo.height

    onVisibleItemsChanged: {
      //console.log('visible items: ' + visibleItems)
    }

    onHiddenItemsChanged: {
      //console.log('hidden items: ' + hiddenItems)
    }

    // main caption/title of this particular instance
    // configurable by the user in preferences (ToDo!)
    // provided to help distinguish between instances if many are used
    Text {
      id: mainCaption
      property alias configuredText: mainCaptionTextInputContainer.text
      text: "<h3>" + configuredText + "</h3>"
      font.weight: Font.Bold
      horizontalAlignment: Text.AlignHCenter
      smooth: true
      style: Text.Sunken
      wrapMode: Text.Wrap
      color: plasmaTheme.textColor
      anchors {
        top: parent.top
        left: parent.left
        right: parent.right
      }
      property alias editing: mainCaptionTextInputContainer.visible

      onEditingChanged: {
        // if we just stopped editing, save the config
        if (editing == false) {
          plasmoid.writeConfig("TaskerLabel", configuredText);
        }
      }

      // text input for changing plasmoid name
      ImprovedTextInput {
        id: mainCaptionTextInputContainer
        text: "Tasker"
      }
    }

    Column {
      id: todosContainer
      anchors {
        top: mainCaption.bottom
        left:parent.left
        right:parent.right
        rightMargin:1
      }
      property bool isColumn: true
    }

    // add-a-todo button
    Button {
      id: globalAddToDo
      text: i18n("add")
      smooth: true
      height: Math.max(
        (mainContainer.height - mainCaption.height) / ( mainContainer.visibleItems + 1 ) - 3,
        29
      )
      anchors {
        left: parent.left
        right: parent.right
        bottom: parent.bottom
        rightMargin:1
      }
      color: plasmaTheme.buttonBackgroundColor
      shadeColor: plasmaTheme.highlightColor
      hoverColor: plasmaTheme.buttonHoverColor
      textColor: plasmaTheme.buttonTextColor
      onClicked: addToDoItem(todosContainer)
    }
  }
}