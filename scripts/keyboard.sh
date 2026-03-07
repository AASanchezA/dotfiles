#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# Requirements:
#   rofi
# Description:
#   Use rofi to change keyboard layout
# Usage:
#   keyboard.sh
# -----------------------------------------------------------------------------
# Script:

declare -A LAYOUTS

LAYOUTS=(
  ["german"]="de"
  ["spanish"]="es"
  ["english"]="us"
)

# List for rofi
gen_list() {
    for i in "${!LAYOUTS[@]}"
    do
      echo "$i"
    done
}

main() {
  # Pass the list to rofi
  layout=$( (gen_list) | rofi -dmenu -matching fuzzy -no-custom -location 0 -p "Search > " )

  if [[ -n "$layout" ]]; then
      setlayout=${LAYOUTS[$layout]}
      setxkbmap $setlayout
      notify-send --app-name="DOOM" "Keyboard layout: $setlayout"
  else
    exit
  fi
}

main


exit 0
