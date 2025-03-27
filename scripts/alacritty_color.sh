#!/usr/bin/env bash

# TODO Improve list of colors
COLORS=("#031a40" "#4d0000" "#183f18" "#1e381e" "#656765" "#585a58" "#4c4d4c" "#3f403f" "#323432" "#2c2d3c" "#262726")
let MAX_COLORS_INDEX=${#COLORS[@]}-1
INDEX=$(shuf -i 0-$MAX_COLORS_INDEX -n 1 -z)
echo ${COLORS[$INDEX]}



