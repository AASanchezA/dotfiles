#!/bin/bash
cd "$(dirname "$0")"
for a in */LC_MESSAGES/*.po; do
	echo "recompiling $a ..."
	b="$(echo $a | perl -p -e 's/\.po$//').mo"
	msgfmt $a -o $b
done