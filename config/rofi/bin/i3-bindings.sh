#!/usr/bin/env bash

if [ x"$@" = x"quit" ]
then
	exit 0
fi

echo -en "aap\0icon\x1ffolder\x1finfo\x1ftest\n"
#echo "quit"
/home/andres/.cargo/bin/i3-bindings --csv |awk -F';' '{print $1 $3 $4 $5"\0icon\x1ffolder\x1finfo\x1ftest\\n"}'
