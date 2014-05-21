/*
 *   Matrix Plasmoid (Functions-File) - an other kool widget for KDE
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

var matrixIsDead = false;
var matrixTimer = null;
var startStopDiv = null;
var plasmoidWidth = null;
var plasmoidHeight = null;
var clickButtonToStart = false;
var speedDelay = 0;
var speedDelayAfterClicked = null;
var startMessage = "";
var stopMessage = "";
var threeDEffect = false;
var wakeUpToStart = false;
var showMonitor   = false;
var customColorSettings = false;

var customCharacterColor = "";
var customBackgroundColor = "";

var red   = "";
var green = "";
var blue  = "";

var red_background   = "";
var green_background = "";
var blue_background  = "";

var customRGB_TheBigOne = "";

var customRed_standard = "";
var customRed_mini     = "";
var customRed_tiny     = "";

var customGreen_standard = "";
var customGreen_mini     = "";
var customGreen_tiny     = "";

var customBlue_standard = "";
var customBlue_mini     = "";
var customBlue_tiny     = "";

var customRGB_standard_present = "";
var customRGB_mini_present = "";
var customRGB_tiny_present = "";

var customRGB_standard_past = "";
var customRGB_mini_past     = "";
var customRGB_tiny_past     = "";

var customRGB_standard_nDead = "";
var customRGB_mini_nDead     = "";
var customRGB_tiny_nDead     = "";


var transparency = false;
var fontSize = 12;
var lineHeight = 12;
var columnPixelWidth = 15;
var numberOfRowsBeforeVisible = 3;
var numberOfRowsAfterVisible  = 1;
var topOffset = -(lineHeight*numberOfRowsBeforeVisible) + 2;
var canvasDiv = null;
var initString = "M⌈Ü7ΔV3€[S£¥]ΠΔPΘΛX∀YΨ";
var matrixString = "";
var canvasWidth = 0;
var canvasHeight = 0;
var column = null; //Array
var columnDiv = null; //Array
var numberOfColumns = 0;
var numberOfRows = 0;

//Timer Function Things
var timerFunction = null;
var numberOfFinishedColumnsBeforeStringReset = 8;
var visibleLength = 0;
var newString = "";
var otherColumnIndex = 0; //to switch the character and visible length depending on an other column

var transformSpeedToDelay = function( speed, maxSpeed ) {
    var delay = 0;
    var scaleFactor = 10;

    if( speed > maxSpeed ) {
        speed = maxSpeed;
    }

    delay = (maxSpeed - speed) * scaleFactor;

    return delay;
}

// opacity = [0..1]
var getCustomColorOpacityFake = function( color, backgroundColor, opacity)
{
	color = color * opacity;
	
	backgroundColor = backgroundColor * (1 - opacity);
	
	var resultColor = Math.floor( color + backgroundColor );
	
	return resultColor;
}

var getZValueColor = function( position, maxPosition, startColor, endColor ) {
    var range = endColor - startColor;
    var percentualPosition = position / maxPosition;
    var newValue = startColor + Math.floor( range * percentualPosition );
    
    return newValue;
}

var getZValueOpacity = function( position, maxPosition, startOpacity, endOpacity ) {
    var range = endOpacity - startOpacity;
    var percentualPosition = position / maxPosition;
    var newValue = startOpacity + ( range * percentualPosition );
    /*newValue *= 10;
    newValue = Math.floor(newValue);
    newValue /= 10;*/
    
    if( newValue > 1) {
	newValue = 1.0;
    }
    
    if( newValue < 0) {
	newValue = 0.0;
    }
    
    return newValue;
}


var constructColumn = function( d, s, i ) {
	this.divName = d;
	this.div = document.getElementById ( this.divName );
	this.posX = 0;
	this.posY = 0;
	this.new3dXPosition = null;
	this.new3dColumnIndexExtraScale = 0;
	this.string = s;
	this.defaultString = this.string;
	this.columnIndex = i;
	this.output = "";
	this.position = (this.columnIndex * 5) % this.string.length;
	this.lastStartPosition = 0;
	this.visibleLength = this.string.length;
	this.columnWasFinishedCount = 0;
	this.isSmallColumn = false;
	this.smallColumnSpeedSwitch = 0;
	this.isTinyColumn = false;
	this.tinyColumnSpeedSwitch = 0;

	this.variableIndexInc = 0;

//     if( (this.columnIndex/2) > (numberOfColumns/2)  ) {
//         this.new3dColumnIndex = this.columnIndex - Math.floor( numberOfColumns / 2 );
//     } else {
//         this.new3dColumnIndex = -Math.floor( numberOfColumns / 2 ) + this.columnIndex;
//     }

//     this.new3dColumnIndex *= 2;

	this.setPosition = function( posX, posY ) {
		if( posX != null) {
			this.posX = posX;
		}

		if( posY != null) {
			this.posY = posY;
		}

		this.div.style.left = Math.floor(this.posX) + "px";
		this.div.style.top  = Math.floor(this.posY) + "px";
	}

	this.setString = function( s ) {
		this.string = s;
		this.defaultString = this.string;
	}

	this.resetString = function() {
		this.string = this.defaultString;
	}

	this.createOutput = function() {

		if( threeDEffect ) {
			new3dColumnIndexExtraScale = (this.posX) > (canvasWidth/2) ? (this.posX - canvasWidth/2) : -(canvasWidth/2 - this.posX);
			new3dColumnIndexExtraScale *= (this.position/2);
			new3dColumnIndexExtraScale /= 1000;
		}

		this.output = "";
		var styleClass = "";

		var variableIndex = 0;
		var newString = "";

		if( ((this.columnIndex + this.lastStartPosition) % 5) == 1 ) {
			this.isSmallColumn = true;
			this.isTinyColumn  = false;
			if( threeDEffect ) {
				this.div.style.zIndex = "" + (1000 + this.position);
				this.div.style.fontSize = "12px";
				this.div.style.lineHeight = (lineHeight) + "px";
			}
		} else if( ((this.columnIndex + this.lastStartPosition) % 3) == 1 ) {
			this.isTinyColumn = true;
			this.isSmallColumn = false;
			if( threeDEffect ) {
				this.div.style.zIndex = "" + (this.position);
				this.div.style.fontSize = "11px";
				this.div.style.lineHeight = (lineHeight-1) + "px";
				if( ((this.columnIndex + this.lastStartPosition) % 2) == 0 ) {
					this.div.style.fontSize = "12px";
					this.div.style.lineHeight = (lineHeight) + "px";
				}
			}
		} else {
			this.isTinyColumn = false;
			this.isSmallColumn = false;
			if( threeDEffect ) {
				this.div.style.zIndex = "" + (2000 + this.position);
				this.div.style.fontSize = "14px";
				this.div.style.lineHeight = (lineHeight+2) + "px";
			}
		}

		/*if( this.isSmallColumn && (this.smallColumnSpeedSwitch < 0) ) {
			this.smallColumnSpeedSwitch++;
			this.position--;
		} else*/
		if( this.isTinyColumn && (this.tinyColumnSpeedSwitch == 0) ) {
			this.tinyColumnSpeedSwitch++;
			this.position--;
			this.setPosition( this.posX, this.posY - 1 );

			if( threeDEffect ) {
				this.new3dXPosition = this.posX + (new3dColumnIndexExtraScale);
			}
			if( ((this.columnIndex + this.lastStartPosition) % 2) == 0 ) {
				this.posY++;
			}
			this.setPosition( this.new3dXPosition, --this.posY );
		} else {
			this.div = document.getElementById ( this.divName );
			if( (!this.isSmallColumn && !this.isTinyColumn) ) { //normal
				if( threeDEffect ) {
					this.new3dXPosition = this.posX + (3*new3dColumnIndexExtraScale);
					if( ((this.columnIndex + this.lastStartPosition) % 4) == 1 ) {
						//this.div.style.color = "#44ff22";
						this.div.style.fontSize = (14 + Math.floor(this.position/8) ) + "px";
						this.div.style.lineHeight = (14 + Math.floor(this.position/8) ) + "px";
						this.posY -= Math.floor(this.position/8)*4;
						this.div.style.zIndex = "" + (3000 + this.position);
					}
				} 
				this.setPosition( this.new3dXPosition, this.posY + 1 );
			} else 
			if( (this.isTinyColumn) ) { //tiny
				if( threeDEffect ) {
					this.new3dXPosition = this.posX + (new3dColumnIndexExtraScale);
				}
				if( ((this.columnIndex + this.lastStartPosition) % 2) == 0 ) {
					this.posY++;
				}
				this.setPosition( this.new3dXPosition, --this.posY );

			} else {
				if( threeDEffect ) { //small
					this.new3dXPosition = this.posX + (2*new3dColumnIndexExtraScale);
				}
				this.setPosition( this.new3dXPosition, null );
			}


			this.smallColumnSpeedSwitch = 0;
			this.tinyColumnSpeedSwitch  = 0;

			for( var i = 0; i < this.string.length; i++ ) {
				if( i < this.position ) {
					if( i <= (this.position - this.visibleLength) ) {
						if( i == (this.position - this.visibleLength) ) {
							styleClass = "nearlyDead";
						} else {
							styleClass = "dead";
						}
					} else {
						styleClass = "past"
					}
				} else if ( i == this.position ) {
					styleClass = "present";
				} else {
					styleClass = "future";
				}


				if( this.isSmallColumn) {
					styleClass += " mini";
				} else if( this.isTinyColumn) {
					styleClass += " tiny";
				}

				if( (i == this.string.length-1) && ( !this.isSmallColumn ) ) {
					if( styleClass == "past tiny" ) {
						styleClass = "present mini";
					}

					if( styleClass == "past" ) {
						styleClass = "present big";
					}

					//create a new string for the matrix

					this.variableIndexInc++;
					variableIndex = (this.variableIndexInc % this.string.length);
					newString = this.string.substring(0, (this.string.length-1) );
					newString += column[0].string[variableIndex];
					this.string = newString;

					//this.setPosition( this.posX, this.posY - 1 );
					
				}
				
				if ( threeDEffect && (styleClass == "past" || styleClass == "past mini" || styleClass == "past tiny") ) {
					var zIndexColor = "";
					
					if( styleClass == "past tiny") {
					zIndexColor = "rgb(" 
						+ 0 + ", "
						+ getZValueColor(this.position, numberOfRows, 15, 140) + ", "
						+ 0 + ")";
					
					} else if( styleClass == "past mini") {
					zIndexColor = "rgb(" 
						+ 0 + ", "
						+ getZValueColor(this.position, numberOfRows, 70, 220) + ", "
						+ 0 + ")";
					
					} else if( styleClass == "past") {
					zIndexColor = "rgb(" 
						+ 31 + ", "
						+ getZValueColor(this.position, numberOfRows, 150, 255) + ", "
						+ 15 + ")";
					
					}
					this.output += "<span class=\"" + styleClass + "\" style=\"color:" + zIndexColor + "\">" + this.string[i] + "</span><br />";
				} else {
					this.output += "<span class=\"" + styleClass + "\">" + this.string[i] + "</span><br />";
				}
				
			} // end for
		
			this.div.innerHTML = this.output;
		} // end else
	}
}

var constructColumnCustom = function( d, s, i ) {
	this.divName = d;
	this.div = document.getElementById ( this.divName );
	this.posX = 0;
	this.posY = 0;
	this.new3dXPosition = null;
	this.new3dColumnIndexExtraScale = 0;
	this.string = s;
	this.defaultString = this.string;
	this.columnIndex = i;
	this.output = "";
	this.position = (this.columnIndex * 5) % this.string.length;
	this.lastStartPosition = 0;
	this.visibleLength = this.string.length;
	this.columnWasFinishedCount = 0;
	this.isSmallColumn = false;
	this.smallColumnSpeedSwitch = 0;
	this.isTinyColumn = false;
	this.tinyColumnSpeedSwitch = 0;

	this.variableIndexInc = 0;

	this.setPosition = function( posX, posY ) {
		if( posX != null) {
			this.posX = posX;
		}

		if( posY != null) {
			this.posY = posY;
		}

		this.div.style.left = Math.floor(this.posX) + "px";
		this.div.style.top  = Math.floor(this.posY) + "px";
	}

	this.setString = function( s ) {
		this.string = s;
		this.defaultString = this.string;
	}

	this.resetString = function() {
		this.string = this.defaultString;
	}

	this.createOutput = function() {

		if( threeDEffect ) {
			new3dColumnIndexExtraScale = (this.posX) > (canvasWidth/2) ? (this.posX - canvasWidth/2) : -(canvasWidth/2 - this.posX);
			new3dColumnIndexExtraScale *= (this.position/2);
			new3dColumnIndexExtraScale /= 1000;
		}

		this.output = "";
		var styleClass = "";

		var variableIndex = 0;
		var newString = "";

		if( ((this.columnIndex + this.lastStartPosition) % 5) == 1 ) {
			this.isSmallColumn = true;
			this.isTinyColumn  = false;
			if( threeDEffect ) {
				this.div.style.zIndex = "" + (1000 + this.position);
				this.div.style.fontSize = "12px";
				this.div.style.lineHeight = (lineHeight) + "px";
			}
		} else if( ((this.columnIndex + this.lastStartPosition) % 3) == 1 ) {
			this.isTinyColumn = true;
			this.isSmallColumn = false;
			if( threeDEffect ) {
				this.div.style.zIndex = "" + (this.position);
				this.div.style.fontSize = "11px";
				this.div.style.lineHeight = (lineHeight-1) + "px";
				if( ((this.columnIndex + this.lastStartPosition) % 2) == 0 ) {
					this.div.style.fontSize = "12px";
					this.div.style.lineHeight = (lineHeight) + "px";
				}
			}
		} else {
			this.isTinyColumn = false;
			this.isSmallColumn = false;
			if( threeDEffect ) {
				this.div.style.zIndex = "" + (2000 + this.position);
				this.div.style.fontSize = "14px";
				this.div.style.lineHeight = (lineHeight+2) + "px";
			}
		}

		/*if( this.isSmallColumn && (this.smallColumnSpeedSwitch < 0) ) {
			this.smallColumnSpeedSwitch++;
			this.position--;
		} else*/ if( this.isTinyColumn && (this.tinyColumnSpeedSwitch == 0) ) {
			this.tinyColumnSpeedSwitch++;
			this.position--;
			this.setPosition( this.posX, this.posY - 1 );

			if( threeDEffect ) {
				this.new3dXPosition = this.posX + (new3dColumnIndexExtraScale);
			}
			if( ((this.columnIndex + this.lastStartPosition) % 2) == 0 ) {
				this.posY++;
			}
			this.setPosition( this.new3dXPosition, --this.posY );
		} else {
			this.div = document.getElementById ( this.divName );
			if( (!this.isSmallColumn && !this.isTinyColumn) ) { //normal
				if( threeDEffect ) {
					this.new3dXPosition = this.posX + (3*new3dColumnIndexExtraScale);
					if( ((this.columnIndex + this.lastStartPosition) % 4) == 1 ) {
						//this.div.style.color = "#44ff22";
						this.div.style.fontSize = (14 + Math.floor(this.position/8) ) + "px";
						this.div.style.lineHeight = (14 + Math.floor(this.position/8) ) + "px";
						this.posY -= Math.floor(this.position/8)*4;
						this.div.style.zIndex = "" + (3000 + this.position);
					}
				} 
				this.setPosition( this.new3dXPosition, this.posY + 1 );
			} else 
			if( (this.isTinyColumn) ) { //tiny
				if( threeDEffect ) {
					this.new3dXPosition = this.posX + (new3dColumnIndexExtraScale);
				}
				if( ((this.columnIndex + this.lastStartPosition) % 2) == 0 ) {
					this.posY++;
				}
				this.setPosition( this.new3dXPosition, --this.posY );

			} else {
				if( threeDEffect ) { //small
					this.new3dXPosition = this.posX + (2*new3dColumnIndexExtraScale);
				}
				this.setPosition( this.new3dXPosition, null );
			}


			this.smallColumnSpeedSwitch = 0;
			this.tinyColumnSpeedSwitch  = 0;

			var presentColor = "";

			for( var i = 0; i < this.string.length; i++ ) {
				if( i < this.position ) {
					if( i <= (this.position - this.visibleLength) ) {
						if( i == (this.position - this.visibleLength) ) {
							styleClass = "nearlyDead";
						} else {
							styleClass = "dead";
						}
					} else {
						styleClass = "past"
					}
				} else if ( i == this.position ) {
					styleClass = "present";
				} else {
					styleClass = "future";
				}


				if( this.isSmallColumn) {
					styleClass += " mini";
				} else if( this.isTinyColumn) {
					styleClass += " tiny";
				}

				if( (i == this.string.length-1) && ( !this.isSmallColumn ) ) {
					if( styleClass == "past tiny" ) {
						styleClass = "present mini";
					}

					if( styleClass == "past" ) {
						styleClass = "present big";
					}

					//create a new string for the matrix

					this.variableIndexInc++;
					variableIndex = (this.variableIndexInc % this.string.length);
					newString = this.string.substring(0, (this.string.length-1) );
					newString += column[0].string[variableIndex];
					this.string = newString;

					//this.setPosition( this.posX, this.posY - 1 );
				}
                
				if ( threeDEffect && ( styleClass == "past" || styleClass == "past mini" || styleClass == "past tiny" ) ) {
					var zIndexColor = "";
					var zIndexOpacity = "";
				
					if( styleClass == "past tiny") {
						zIndexOpacity = getZValueOpacity(this.position, numberOfRows, 0.2, 0.6);
					} else if( styleClass == "past mini") {
						zIndexOpacity = getZValueOpacity(this.position, numberOfRows, 0.4, 0.8);
					} else if( styleClass == "past") {
						zIndexOpacity = getZValueOpacity(this.position, numberOfRows, 0.6, 1.0);
					}
					
					presentColor = "rgb(" + getCustomColorOpacityFake( red, red_background, zIndexOpacity )  + ", " + getCustomColorOpacityFake( green, green_background, zIndexOpacity ) + ", " + getCustomColorOpacityFake( blue, blue_background, zIndexOpacity ) + ")";
					
					this.output += "<span style=\"color:" + presentColor + "\">" + this.string[i] + "</span><br />";
				} else if ( styleClass == "past" || styleClass == "past mini" || styleClass == "past tiny" || styleClass == "nearlyDead" || styleClass == "nearlyDead mini" || styleClass == "nearlyDead tiny" ) {
					if( styleClass == "past") {
						presentColor = customRGB_standard_past;
					} else if( styleClass == "past tiny") {
						presentColor = customRGB_tiny_past;
					} else if( styleClass == "past mini") {
						presentColor = customRGB_mini_past;
					} else if( styleClass == "nearlyDead") {
						presentColor = customRGB_standard_nDead;
					} else if( styleClass == "nearlyDead tiny") {
						presentColor = customRGB_tiny_nDead;
					} else if( styleClass == "nearlyDead mini") {
						presentColor = customRGB_mini_nDead;
					}
					this.output += "<span style=\"color:" + presentColor + "\">" + this.string[i] + "</span><br />";
				} else if ( styleClass == "present" || styleClass == "present mini" || styleClass == "present tiny" || styleClass == "present big" ) {
					if( styleClass == "present") {
						presentColor = customRGB_standard_present;
					} else if( styleClass == "present tiny") {
						presentColor = customRGB_tiny_present;
					} else if( styleClass == "present mini") {
						presentColor = customRGB_mini_present;
					} else if( styleClass == "present big") {
						presentColor = customRGB_TheBigOne;
					}
					this.output += "<span style=\"color:" + presentColor + "\">" + this.string[i] + "</span><br />";
				} else {
					//future or dead
					this.output += "<span class=\"" + styleClass + "\">" + this.string[i] + "</span><br />";
				}
			} // end for

			this.div.innerHTML = this.output;
		} // end else
	}
}


var startStopTheMatrix = function() {

    var messageFontSize = fontSize;
    if( canvasWidth < 161 ) {
        messageFontSize = 8;
        if( canvasWidth < 119 ) {
            messageFontSize = 6;
        }
    }
    var messageStart = ""
        + "<div style=\"margin-top: " + (canvasHeight/2 - 6 ) + "px;\">"
            + "<span style=\"border:1px solid "
            + customCharacterColor
            + "; background-color: "
            + customBackgroundColor
            + "; padding: 5px;white-space: nowrap;font-size:" + messageFontSize + "px\">";

    var message = "";
    var messageEnd = ""
            + "</span>"
        + "</div>";


    if( clickButtonToStart ) {
        clearTimeout( matrixTimer );
        message = startMessage;
        if( message != "undefined" ) {
            startStopDiv.innerHTML = messageStart + message + messageEnd;
			showMonitorOrNot( showMonitor );
			
        }
        clickButtonToStart = false;
        //window.onresize = sizeChanged();
    } else {
        if( !matrixIsDead ) {
            matrixIsDead = true;
            clearTimeout( matrixTimer );
            message = stopMessage;
            if( message != "undefined" ) {
                startStopDiv.innerHTML = messageStart + message + messageEnd;
			showMonitorOrNot( showMonitor );
            }
        } else {
            matrixIsDead = false;
            startStopDiv.innerHTML = "";
			showMonitorOrNot( showMonitor );
            //init();
            timerFunction();
        }
    }
}

var getStringSetToMinLength = function( s ) {
    //the string should be able to consist of min. "minCharCount" characters
    var minCharCount = 1000;

    var factor = Math.floor( minCharCount / s.length );
    
    var initS = s;
    for( var i=0; i < factor; i++) {
        s += initS;
    }

    return s;
}

var initializeMatrix = function() {

    canvasDiv = document.getElementById ( "canvas" );
    canvasDiv.style.fontSize   = fontSize   + "px";
    canvasDiv.style.lineHeight = lineHeight + "px";

    canvasDiv.style.color = customCharacterColor;
    canvasDiv.style.backgroundColor = customBackgroundColor;
	
    if (transparency) {
	canvasDiv.style.backgroundColor = "transparent";
    }

    canvasWidth  = canvasDiv.offsetWidth;
    canvasHeight = canvasDiv.offsetHeight;
    
    numberOfRows    = Math.floor( canvasHeight / lineHeight ) + numberOfRowsBeforeVisible + numberOfRowsAfterVisible;
    numberOfRows   += 4;
    numberOfColumns = Math.floor( canvasWidth  / columnPixelWidth ) + 1;

    //console.log( numberOfRows + " " + numberOfColumns );
    
    initString = getStringSetToMinLength( initString );

    matrixString = initString.substring( 0, numberOfRows );

    column = new Array();
    columnDiv = new Array();
    var columnDivName = "";
    var style = "";
    var posX = 0;
    var posY = topOffset;
    canvasDiv.innerHTML = "";

    //alert( numberOfColumns );
    for( var i = 0; i < numberOfColumns; i++) {

        columnDivName = "column_" + i;

        style += "position: absolute; ";
        style += "width: " + columnPixelWidth + "px; ";
        style += "top: "   + posY + "px; ";
        style += "left: "  + posX + "px; ";
        //style += "overflow:hidden;";
        style += "text-align: center";

        canvasDiv.innerHTML += "<div id=\"" + columnDivName + "\" style=\"" + style + "\"></div>\n";

        columnDiv[i] = document.getElementById ( columnDivName );
        //columnDiv[i].innerHTML = "GGG";

        posX = i*columnPixelWidth;
	if( !customColorSettings ) {
	    column[i] = new constructColumn( columnDivName, matrixString, i );
	} else {
	    column[i] = new constructColumnCustom( columnDivName, matrixString, i );
	}

        column[i].setPosition( posX, posY );
        column[i].position = numberOfRows + numberOfRows -1;
    }

    canvasDiv.innerHTML += "<div id=\"startStop\" onclick=\"startStopTheMatrix()\"></div>";

	//canvasDiv.innerHTML += "<div id=\"startStop\" onclick=\"startStopTheMatrix()\"><div id=\"monitor\"><img src=\"monitor.png\" /></div></div>";

    startStopDiv = document.getElementById ( "startStop" );
    startStopDiv.style.position="absolute";
    startStopDiv.style.top = "0px";
    startStopDiv.style.left = "0px";
    startStopDiv.style.width = canvasWidth + "px";
    startStopDiv.style.height = canvasHeight + "px";
    startStopDiv.style.textAlign = "center";
    startStopDiv.style.zIndex = "10000";
	showMonitorOrNot( showMonitor );
    
}

var sizeChanged = function() {
    initializeMatrix();
}

var init = function() {
    var speed = parseInt( getGetVar( "speed" ) );
    var maxSpeed = parseInt( getGetVar( "s_max" ) );
    speedDelayAfterClicked =  transformSpeedToDelay( speed, maxSpeed );
    speedDelay = speedDelayAfterClicked;
    startMessage = getGetVar( "m_start");
    stopMessage  = getGetVar( "m_stop");
    var getVarInitString = getGetVar( "string" );
    if( getVarInitString !== "undefined" ) {
        initString = getGetVar( "string" );
    }
    if( getGetVar( "effect_3d" ) == "true" ) {
        threeDEffect = true;
    }
    if( getGetVar( "transparency" ) == "true" ) {
        transparency = true;
    }
	if( getGetVar( "wake_up" ) == "true" ) {
		wakeUpToStart = true;
		clickButtonToStart = true;
	}
	if( getGetVar( "monitor_show" ) == "true" ) { //default: true
		showMonitor = true;
	}
    if( getGetVar( "custom_color_settings" ) == "true" ) {
        customColorSettings = true;
    }

    if( customColorSettings ) {
		customCharacterColor  = "#" + getGetVar( "custom_character_color" );
		customBackgroundColor = "#" + getGetVar( "custom_background_color" );
			
		
		//standard, mini, tiny
		
		red   = getRGBFromHex( customCharacterColor, 1 );
		green = getRGBFromHex( customCharacterColor, 2 );
		blue  = getRGBFromHex( customCharacterColor, 3 );

		red_background   = getRGBFromHex( customBackgroundColor, 1 );
		green_background = getRGBFromHex( customBackgroundColor, 2 );
		blue_background  = getRGBFromHex( customBackgroundColor, 3 );
		
		//standard, mini, tiny ("past colors" => after first letter)
		customRed_standard   = red;
		customGreen_standard = green;
		customBlue_standard  = blue;
		
		customRed_mini       = getCustomColorOpacityFake( red,   red_background,   0.65 );
		customGreen_mini     = getCustomColorOpacityFake( green, green_background, 0.65 );
		customBlue_mini      = getCustomColorOpacityFake( blue,  blue_background,  0.65 );
		
		customRed_tiny       = getCustomColorOpacityFake( red,   red_background,   0.4 );
		customGreen_tiny     = getCustomColorOpacityFake( green, green_background, 0.4 );
		customBlue_tiny      = getCustomColorOpacityFake( blue,  blue_background,  0.4 );

		customRGB_standard_past = "rgb(" + customRed_standard + ", " + customGreen_standard + ", " + customBlue_standard + ")";
		customRGB_mini_past     = "rgb(" + customRed_mini     + ", " + customGreen_mini     + ", " + customBlue_mini + ")";
		customRGB_tiny_past     = "rgb(" + customRed_tiny     + ", " + customGreen_tiny     + ", " + customBlue_tiny + ")";

		customRGB_standard_nDead = "rgb(" + customRed_mini + ", " + customGreen_mini + ", " + customBlue_mini + ")";
		customRGB_mini_nDead     = "rgb(" + customRed_tiny     + ", " + customGreen_tiny     + ", " + customBlue_tiny + ")";
		customRGB_tiny_nDead = "rgb(" + getCustomColorOpacityFake( red, red_background, 0.3 )  + ", " + getCustomColorOpacityFake( green, green_background, 0.3 ) + ", " + getCustomColorOpacityFake( blue, blue_background, 0.3 ) + ")";

		//calculate "present colors"
		//if( colorIsBrighter( customCharacterColor, customBackgroundColor ) ) {
		var newRed   = 0 + red   + Math.floor( (255 - red)   / 1.5 );
		var newGreen = 0 + green + Math.floor( (255 - green) / 1.5 );
		var newBlue  = 0 + blue  + Math.floor( (255 - blue)  / 1.5 );
		
		// The Big Ones ( = present = first letter)
		customRGB_standard_present = "rgb(" + newRed + ", " + newGreen + ", " + newBlue + ")";
		customRGB_mini_present = "rgb(" + getCustomColorOpacityFake( red, red_background, 0.85 )  + ", " + getCustomColorOpacityFake( green, green_background, 0.85 ) + ", " + getCustomColorOpacityFake( blue, blue_background, 0.85 ) + ")";
		customRGB_tiny_present = "rgb(" + getCustomColorOpacityFake( red, red_background, 0.6 )  + ", " + getCustomColorOpacityFake( green, green_background, 0.6 ) + ", " + getCustomColorOpacityFake( blue, blue_background, 0.6 ) + ")";
		
		newRed   = 0 + newRed   + Math.floor( (255 - newRed)   / 1.2 );
		newGreen = 0 + newGreen + Math.floor( (255 - newGreen) / 1.2 );
		newBlue  = 0 + newBlue  + Math.floor( (255 - newBlue)  / 1.2 );
		
		customRGB_TheBigOne  = "rgb(" + newRed + ", " + newGreen + ", " + newBlue + ")";
	} else {
		customCharacterColor  = "#00ff00";
		customBackgroundColor = "#000000";
	}
		
	initializeMatrix();
	timerFunction();
}

timerFunction = function() {
    if( !matrixIsDead ) {
        for( var i = 0; i < numberOfColumns; i++ ) {

            if( column[i].position < ( column[i].string.length + column[i].visibleLength) ) {
                column[i].position++;
                columnDiv[i].innerHTML = column[i].createOutput();
            
            } else {

                visibleLength = ((i + column[i].lastStartPosition) *3) % numberOfRows;

                otherColumnIndex = visibleLength % numberOfColumns;
                otherColumnIndex = column[otherColumnIndex].lastStartPosition;

                column[i].position = 0;

                if( visibleLength < 4 ) {
                    visibleLength = 5;
                }

                column[i].visibleLength = visibleLength;

                //create a new string for the matrix
                newString = column[i].string.substring(1);
                newString += column[otherColumnIndex].string[visibleLength];
                column[i].string = newString;

                column[i].lastStartPosition = column[i].columnWasFinishedCount % visibleLength;

                column[i].columnWasFinishedCount++;

                if( column[i].columnWasFinishedCount == numberOfFinishedColumnsBeforeStringReset ) {
                    column[i].resetString();
                    column[i].visibleLength = numberOfRows; //just for fun: to get a long chain
                    column[i].columnWasFinishedCount = 0;
                }

                if( column[i].columnWasFinishedCount == 3 ) {
                    if( clickButtonToStart ) {
                        startStopTheMatrix();
                        matrixIsDead = true;
                        speedDelay = speedDelayAfterClicked;                            
                    }
                }

                column[i].setPosition( i*columnPixelWidth, topOffset );

                if( (canvasWidth != canvasDiv.offsetWidth) || (canvasHeight != canvasDiv.offsetHeight)) {
                    sizeChanged();
                }
            }
        }

        matrixTimer = window.setTimeout(timerFunction, speedDelay);
    }
}

var getVarsArray = new Array();
var getVarsString= document.location.search.substr(1,document.location.search.length);
if( getVarsString != "" ) {
    var gArr = getVarsString.split("&");
    for( i=0; i<gArr.length; ++i) {
        var v = "";
        var vArr = gArr[i].split("=");
        if( vArr.length > 1 ){
            v = vArr[1];
        }
        getVarsArray[unescape(vArr[0])] = unescape(v);
    }
}

function getGetVar(v) {
    if(!getVarsArray[v]){
        return 'undefined';
    }

    return getVarsArray[v];
}

function getRGBFromHex( rgbString, colorId ) {
    //rgbSttring: #1289ab
    //colorId: 1 = red, 2 = blue, 3 = green
    var red   = rgbString.substr(1,2);
    var green = rgbString.substr(3,2);
    var blue  = rgbString.substr(5,2);

    switch( colorId ) {
    case 1:
	return parseInt( red, 16 );
	break;
    case 2:
	return parseInt( green, 16 );
	break;
    case 3:
	return parseInt( blue, 16 );
	break;
    }
}

function colorIsBrighter( rgbString1, rgbString2 ) {
    var red1   = getRGBFromHex( rgbString1, 1 );
    var green1 = getRGBFromHex( rgbString1, 2 );
    var blue1  = getRGBFromHex( rgbString1, 3 );
    var red2   = getRGBFromHex( rgbString2, 1 );
    var green2 = getRGBFromHex( rgbString2, 2 );
    var blue2  = getRGBFromHex( rgbString2, 3 );
    
    var sum1 = 0 + red1 + green1 + blue1;
    var sum2 = 0 + red2 + green2 + blue2;

    if( sum1 > sum2 ) {
	return true;
    } else {
	return false;
    }
}

showMonitorOrNot = function( yesOrNo ) {
	if( yesOrNo ) {
		startStopDiv.innerHTML = "<div id=\"monitor\"><img src=\"monitor.png\" /></div>";	
	}
}
