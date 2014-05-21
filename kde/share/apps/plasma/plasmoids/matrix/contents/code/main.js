/*
 *   Matrix Plasmoid (Main-File) - an other kool widget for KDE
 *
 *   Copyright (C) 2010 Gerhard A. Dittes <g-a-d@web.de>
 *
 *   This program is free software; you can redistribute it and/or modify it
 *   under the terms of the GNU General Public License as published by the
 *   Free Software Foundation; either version 3 of the License, or (at your option)
 *   any later version.
 *
 *   This program is distributed in the hope that it will be useful, but
 *   WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 *   or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
 *   more details.
 * 
 *   You should have received a copy of the GNU General Public License along with
 *   this program; if not, see <http://www.gnu.org/licenses/>.
 */

var debugString = "ok\n";
var label1 = null;

label1 = new Label

//plasmoid.hasConfigurationInterface = false;
plasmoid.aspectRatioMode = IgnoreAspectRatio;

var urlWithParameters = "";
var maxSpeed          = 100;

//Read configuration data
var startMessage  = null;
var stopMessage   = null;
var matrixSpeed   = null;
var matrixString  = null;
var threeDEffect  = null;
var showMonitor   = null;
var wakeUpToStart = null;
var showFrame     = null;
var transparency  = null;
var customColorSettings   = false;
var customCharacterColor  = "";
var customBackgroundColor = "";

var calculateFinalSpeed = function( i ) {
    switch( i ) {
        case 0:
            speed = "1";
            break;
        case 1:
            speed = "60";
            break;
        case 2:
            speed = "90";
            break;
        case 3:
            speed = "95";
            break;
        case 4:
            speed = "97";
            break;
        case 5:
            speed = "99";
            break;
        case 6:
            speed = "100";
            break;
        default: // will never be called, I think
            speed = "95";
            break;
    }

    return speed;
}

var readConfigurationData = function(){
	startMessage = plasmoid.readConfig("startMessage");
	stopMessage = plasmoid.readConfig("stopMessage");
	matrixSpeed = calculateFinalSpeed(parseInt(plasmoid.readConfig("speed")));
	matrixString = plasmoid.readConfig("matrixString");
	threeDEffect = plasmoid.readConfig("threeDEffect");
	wakeUpToStart = plasmoid.readConfig("wakeUpToStart");
	showMonitor = plasmoid.readConfig("showMonitor");
	transparency = plasmoid.readConfig("transparency");

	customColorSettings   = plasmoid.readConfig("customColorSettings");
	customCharacterColor  = "" + plasmoid.readConfig("customCharacterColor");  //small workaround
	customBackgroundColor = "" + plasmoid.readConfig("customBackgroundColor"); //small workaround

	showFrame   = plasmoid.readConfig("showFrame");

/*
	debugString += "startMessage: " + startMessage + "\n";
	debugString += "stopMessage: " + stopMessage + "\n";
	debugString += "matrixSpeed: " + matrixSpeed + "\n";
	debugString += "matrixString: " + matrixString + "\n";
	debugString += "threeDEffect: " + threeDEffect + "\n";
	debugString += "wakeUpToStart: " + wakeUpToStart + "\n";
	debugString += "showMonitor: " +  showMonitor+ "\n";
	debugString += "transparency: " + transparency + "\n";
	debugString += "customColorSettings: " + customColorSettings + "\n";
	debugString += "customCharacterColor: " + customCharacterColor + "\n";
	debugString += "customBackgroundColor: " + customBackgroundColor + "\n";
	debugString += "showFrame: " + showFrame + "\n\n";

	label1.text = i18n( debugString )
*/
	if ( showFrame == true ) {
		plasmoid.backgroundHints = DefaultBackground;
		
	} else {
		plasmoid.backgroundHints = NoBackground;
	}
	
	return getUrlWithParameters( matrixSpeed, maxSpeed, startMessage, stopMessage, matrixString, threeDEffect, wakeUpToStart, showMonitor, customColorSettings, customCharacterColor, customBackgroundColor, transparency );
}

var getUrlWithParameters = function ( matrixSpeed, maxSpeed, startMessage, stopMessage, matrixString, threeDEffect, wakeUpToStart, showMonitor, customColorSettings, customCharacterColor, customBackgroundColor, transparency ) {

    var threeDEffectString = "";

    if( threeDEffect == true ) {
        threeDEffectString = "true";
    } else {
        threeDEffectString = "false";
    }

    var wakeUpToStartString = "";

    if( wakeUpToStart == true ) {
        wakeUpToStartString = "true";
    } else {
        wakeUpToStartString = "false";
    }

    var showMonitorString = "";

    if( showMonitor == true ) {
        showMonitorString = "true";
    } else {
        showMonitorString = "false";
    }

	var transparencyString = "";

    if( transparency == true ) {
        transparencyString = "true";
    } else {
        transparencyString = "false";
    }

    var tempUrl   = "";
    var urlString = "";

	if( (customCharacterColor.length == 6) && (customCharacterColor[0] != "#") ) {
		customCharacterColor = "#" + customCharacterColor;
	}

	if( (customBackgroundColor.length == 6) && (customBackgroundColor[0] != "#") ) {
		customBackgroundColor = "#" + customBackgroundColor;
	}

	if( customCharacterColor.length != 7 ) { // workaround
		customCharacterColor  = "#a3fef7";   // custom default, see main.xml
	}

	if( customBackgroundColor.length != 7 ) { // workaround
		customBackgroundColor = "#235966";    //custom default, see main.xml
	}

	customCharacterColor  = customCharacterColor.substring(1, customCharacterColor.length );
	customBackgroundColor = customBackgroundColor.substring(1, customBackgroundColor.length );

	if( customColorSettings == true ) {
		tempUrl = Url( plasmoid.file("scripts", "mainCustom.html" ) );
		urlString = tempUrl.toString 
			+ "?speed="        + matrixSpeed
			+ "&s_max="        + maxSpeed
			+ "&m_start="      + startMessage
			+ "&m_stop="       + stopMessage
			+ "&wake_up="      + wakeUpToStartString
			+ "&monitor_show=" + showMonitor
			+ "&effect_3d="    + threeDEffectString
			+ "&custom_color_settings=true"
			+ "&custom_character_color="  + customCharacterColor
			+ "&custom_background_color=" + customBackgroundColor
			+ "&transparency=" + transparencyString
			+ "&string="       + matrixString;
    } else {
		tempUrl = Url( plasmoid.file("scripts", "main.html" ) );
		urlString = tempUrl.toString 
			+ "?speed="        + matrixSpeed
			+ "&s_max="        + maxSpeed
			+ "&m_start="      + startMessage
			+ "&m_stop="       + stopMessage
			+ "&wake_up="      + wakeUpToStartString
			+ "&monitor_show=" + showMonitor
			+ "&effect_3d="    + threeDEffectString
			+ "&custom_color_settings=false"
			+ "&string="       + matrixString;
    }
    
    /*
      debugString = customCharacterColor + " " + customBackgroundColor + " " + urlString;
      if( label1 ) {
          label1.text = i18n( debugString );
      }
    */
    
    return Url( urlString );
}


//urlWithParameters = readConfigurationData();

layout      = new LinearLayout(plasmoid);
webView     = new WebView();

if (urlWithParameters == "") {
	urlWithParameters = readConfigurationData();
}

webView.url = urlWithParameters;
layout.addItem(webView);

plasmoid.configChanged = function() {
	//read out new config data
	urlWithParameters = readConfigurationData();

	//"restart" the webView
	webView.url = urlWithParameters;
}

//layout.addItem(label1)

