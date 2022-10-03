#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# Requirements:
#   rofi
# Description:
#   Use rofi to search the web.
# Usage:
#   web-search.sh
# -----------------------------------------------------------------------------
# Script:

declare -A URLS

URLS=(
  ["duckduckgo"]="https://www.duckduckgo.com/?q="
  ["archwiki"]="https://wiki.archlinux.org/index.php?search="
  ["google"]="https://www.google.com/search?q="
  #["bing"]="https://www.bing.com/search?q="
  ["github"]="https://github.com/search?q="
  #["goodreads"]="https://www.goodreads.com/search?q="
  ["youtube"]="https://www.youtube.com/results?search_query="
  ["stackoverflow"]="http://stackoverflow.com/search?q="
  #["searchcode"]="https://searchcode.com/?q="
  #["symbolhound"]="http://symbolhound.com/?q="
  #["openhub"]="https://www.openhub.net/p?ref=homepage&query="
  #["superuser"]="http://superuser.com/search?q="
  #["yahoo"]="https://search.yahoo.com/search?p="
  #["askubuntu"]="http://askubuntu.com/search?q="
  #["imdb"]="http://www.imdb.com/find?ref_=nv_sr_fn&q="
  #["rottentomatoes"]="https://www.rottentomatoes.com/search/?search="
  #["piratebay"]="https://thepiratebay.org/search/"
  #["vimawesome"]="http://vimawesome.com/?q="
)

# List for rofi
gen_list() {
    for i in "${!URLS[@]}"
    do
      echo "$i"
    done
}

main() {
  # Pass the list to rofi
  #platform=$( (gen_list) | rofi -dmenu -matching fuzzy -no-custom -location 0 -p "Search > " )
  platform=$( (gen_list) | rofi -dmenu -matching fuzzy -no-custom -location 0 -p "Search > " )

  if [[ -n "$platform" ]]; then
    # use xclip output
    xquery="$(xclip -o -sel clipboard -r)"
    query=$( (echo -e "$xquery") | rofi  -dmenu -matching fuzzy -location 1 -p "Query > " )

    if [[ -n "$query" ]]; then
      url=${URLS[$platform]}$query
      xdg-open "$url"
    else
      exit
    fi

  else
    exit
  fi
}

main


exit 0
