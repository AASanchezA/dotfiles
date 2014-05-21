#!/bin/sh

# Create template file
echo "Creating solar-plasmoid.pot file..."

xgettext --package-version="0.4.1" --no-wrap --copyright-holder="John Ramen" --package-name="solar-system" --keyword=i18n --keyword=i18nc:1c,2 --keyword=i18np:1,2 -o ./solar-system-new.pot ../*.py

# Fixing header (there must be a better way to do this)
echo "Fixing header information..."
sed 's/CHARSET/utf-8/' ./solar-system-new.pot > solar-system-new1.pot ; rm solar-system-new.pot
mv solar-system-new1.pot solar-system.pot

echo "Done."
