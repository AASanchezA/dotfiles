#!/usr/bin/env bash
set -euo pipefail

choice=$(printf "daily\njournal\nidea" | rofi -dmenu -p "org-roam")

case "${choice}" in
  daily)
    emacsclient -n -c -e "(org-roam-dailies-capture-today)" ;;
  journal)
    emacsclient -n -c -e "(andres/org-roam-capture-journal)" ;;
  idea)
    emacsclient -n -c -e "(andres/org-roam-capture-idea)" ;;
  *)
    exit 0 ;;
esac
