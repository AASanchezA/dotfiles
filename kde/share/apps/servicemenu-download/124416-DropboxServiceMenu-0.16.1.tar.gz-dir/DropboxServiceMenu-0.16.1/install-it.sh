#!/bin/bash
sed 's/#SCRIPTS_PATH/SCRIPTS_PATH/g' -i dropbox-scripts/dropbox_menu.sh
sed 's|=dropbox_menu.sh|=`kde4-config --localprefix`/share/kde4/services/ServiceMenus/dropbox-scripts/dropbox_menu.sh|g' -i dropbox_all.desktop
sed 's|=dropbox_menu.sh|=`kde4-config --localprefix`/share/kde4/services/ServiceMenus/dropbox-scripts/dropbox_menu.sh|g' -i dropbox_files.desktop
sed 's|=dropbox_menu.sh|=`kde4-config --localprefix`/share/kde4/services/ServiceMenus/dropbox-scripts/dropbox_menu.sh|g' -i dropbox_directories.desktop
mkdir -p "`kde4-config --localprefix`/share/kde4/services/ServiceMenus/dropbox-scripts"
install -m 644 dropbox_all.desktop "`kde4-config --localprefix`/share/kde4/services/ServiceMenus/"
install -m 644 dropbox_files.desktop "`kde4-config --localprefix`/share/kde4/services/ServiceMenus/"
install -m 644 dropbox_directories.desktop "`kde4-config --localprefix`/share/kde4/services/ServiceMenus/"
install -m 755 dropbox-scripts/* "`kde4-config --localprefix`/share/kde4/services/ServiceMenus/dropbox-scripts/"


