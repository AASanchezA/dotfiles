#!/bin/sh

for i in `ls -d ??`
do
echo "Mergin new $i translations..."
cd $i
msgmerge ./solar-system.po ../solar-system.pot -o solar-system-new.po && mv solar-system-new.po solar-system.po
#msgfmt solar-system.po --output-file solar-system.mo -f
cd ..
done

# Done
echo "Done."
