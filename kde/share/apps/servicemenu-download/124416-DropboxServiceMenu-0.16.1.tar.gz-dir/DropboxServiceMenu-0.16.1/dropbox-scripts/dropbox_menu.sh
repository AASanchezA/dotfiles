#!/bin/bash
#
#     Copyright 2010 Bartosz Iwaniec
#
#     Dropbox_menu.sh
#     A wrapper script around dropbox.py and dropbox-index.py
#
#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program; if not, see http://www.gnu.org/licenses
#     or write to the Free Software Foundation,Inc., 51 Franklin Street,
#     Fifth Floor, Boston, MA 02110-1301  USA
SCRIPTS_PATH=`which dropbox_menu.sh`
SCRIPTS_PATH=`echo "$SCRIPTS_PATH" | sed "s|"${SCRIPTS_PATH##*/}"||g"`
SCRIPTS_PATH="`kde4-config --localprefix`share/kde4/services/ServiceMenus/dropbox-scripts/"
. ${SCRIPTS_PATH}dropbox_menu_translations.sh

fileurl="$2"
#Notifications timeout in ms
error_timeout=20000
success_timeout=5000

if python2 < /dev/null > /dev/null 2>&1; then
    python=python2
fi

#Dropbox path detection
dropbox_path=`${SCRIPTS_PATH}get_dropbox_folder.sh`
#user_key=`sqlite3 ~/.dropbox/config.db 'SELECT value FROM config WHERE key="ns_p2p_key_map"' | awk 'NR==2 {print $0}' | sed 's/L//g'`
echo $dropbox_path
file_in_public="$dropbox_path"/Public/"${fileurl##*/}" #Path to file when it will be placed in dropbox public dir
relative_path=`echo "$fileurl" | sed "s|"$dropbox_path"/||g"` #Relative path to file in $dropbox_path
is_in_public=`echo "$fileurl" | grep "$dropbox_path"/Public` #Check if file is in dropbox public dir
is_in_dropbox=`echo "$fileurl" | grep "$dropbox_path"` #Check if file is in dropbox dir

move() {
    file_exists
    if [ $? == 0 ]; then
	mv -f "$fileurl" "$dropbox_path"/Public
	fileurl=$file_in_public
	is_in_public=`echo "$fileurl" | grep "$dropbox_path"/Public`
	klipper_url
    fi
}

copy() {
    file_exists
    if [ $? == 0 ]; then
	cp -rf "$fileurl" "$dropbox_path"/Public
	fileurl=$file_in_public
	is_in_public=`echo "$fileurl" | grep "$dropbox_path"/Public`
	klipper_url
    fi
}

mailurl() {
    if [ "$is_in_public" != "" ]; then
	generate_url
	xdg-email --subject "$mailurl_subject" --body "$public_link"
    else
	$python ${SCRIPTS_PATH}dropbox-notify.py --icon dialog-error -t $error_timeout Dropbox "$publicurl_error"
    fi
}
gmailurl() {
    if [ "$is_in_public" != "" ]; then
	generate_url
	xdg-open "https://mail.google.com/mail/?ui=2&view=cm&fs=1&su=$mailurl_subject&body=$public_link&shva=1"
    else
	$python ${SCRIPTS_PATH}dropbox-notify.py --icon dialog-error -t $error_timeout Dropbox "$publicurl_error"
    fi
}

share() {
    if [ "$is_in_dropbox" != "" ]; then
	xdg-open https://www.dropbox.com/share_existing/"$relative_path"
    else
	$python ${SCRIPTS_PATH}dropbox-notify.py --icon dialog-error -t $error_timeout Dropbox "$share_error"
    fi
}

revisions() {
    if [ "$is_in_dropbox" != "" ]; then
	xdg-open https://www.dropbox.com/revisions/"$relative_path"
    else
	$python ${SCRIPTS_PATH}dropbox-notify.py --icon dialog-error -t $error_timeout Dropbox "$revisions_error"
    fi
}

klipper_url() {
    if [ "$is_in_public" != "" ]; then
	if [ -d "$fileurl" ]; then
	    $python ${SCRIPTS_PATH}pyndexer.py -R "$fileurl"
	    qdbus org.kde.klipper /klipper org.kde.klipper.klipper.setClipboardContents "`$python ${SCRIPTS_PATH}dropbox.py puburl "$fileurl"/index.html`"
	else
	    qdbus org.kde.klipper /klipper org.kde.klipper.klipper.setClipboardContents "`$python ${SCRIPTS_PATH}dropbox.py puburl "$fileurl"`"
	fi
	    $python ${SCRIPTS_PATH}dropbox-notify.py --icon dialog-ok-apply -t $success_timeout Dropbox "$link_available"
    else
	$python ${SCRIPTS_PATH}dropbox-notify.py --icon dialog-error -t $error_timeout Dropbox "$publicurl_error"
    fi
}

generate_url() {
    if [ -d "$fileurl" ]; then
	$python pyndexer.py -R "$fileurl"
	public_link=`$python ${SCRIPTS_PATH}dropbox.py puburl "$fileurl"/index.html`
    else
	public_link=`$python ${SCRIPTS_PATH}dropbox.py puburl "$fileurl"`
    fi
}

file_exists() {
    if [ -f "$dropbox_path"/Public/"${fileurl##*/}" -o -d "$dropbox_path"/Public/"${fileurl##*/}" ]; then
	kdialog --warningcontinuecancel "$file_exists_text" --title Dropbox
    fi
}

encrypt() {
    if [ "$is_in_public" != "" ]; then
	match=0
	while [ $match -ne 1 ] ; do
	    password=`kdialog --password "$encrypt_password" --title Dropbox`
	    password2=`kdialog --password "$encrypt_rePassword" --title Dropbox`
	    if [ "$password" == "$password2" ]; then
		match=1
	    else
		$python ${SCRIPTS_PATH}dropbox-notify.py --icon dialog-error -t $error_timeout Dropbox "$encrypt_match_error"
	    fi
	done
	if [ "$password" != "" ]; then
	    rm "$fileurl"/".config;"*
	    echo [Options] > "$fileurl"'/.config;'"$password"
	    echo encrypt=true >> "$fileurl"'/.config;'"$password"
	    $python ${SCRIPTS_PATH}dropbox-notify.py --icon dialog-ok-apply -t $success_timeout Dropbox "$encrypt_finish"
	else
	    rm "$fileurl"/".config;"*  #Remove password protection if empty password entered
	fi
	klipper_url
    else
	$python ${SCRIPTS_PATH}dropbox-notify.py --icon dialog-error -t $error_timeout Dropbox "$encrypt_dropbox_error"
    fi
}

lang="$3"
if [ "$3" != "" ]; then
      load_language_en #Fallback to english when there are missing translations
      load_language_$lang
else
      load_language_en
fi

#Dependency checks
if sqlite3 < /dev/null > /dev/null 2>&1 && $python < /dev/null > /dev/null 2>&1 && kdialog < /dev/null > /dev/null && klipper < /dev/null > /dev/null; then
    echo
else
     $python ${SCRIPTS_PATH}dropbox-notify.py --icon dialog-error -t $error_timeout Dropbox "$dependency_error"
     exit 1
fi

case "$1" in
    move) move ;;
    copy) copy ;;
    klipperurl) klipper_url ;;
    revisions) revisions ;;
    mailurl) mailurl ;;
    gmailurl) gmailurl ;;
    share) share ;;
    encrypt) encrypt ;;
esac