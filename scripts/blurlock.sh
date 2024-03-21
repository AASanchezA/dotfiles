#!/bin/bash
# /usr/bin/blurlock

# take screenshot
#import -window root /tmp/screenshot.png

revert() {
	xset dpms 0 0 0
}

# get random image from folder
IMAGE_PATH="$HOME/dotfiles/config/wallpapers/"
IMAGES=($(ls "$IMAGE_PATH"*.jpg))
echo "$IMAGES"
SIZE=${#IMAGES[@]}
INDEX=$(($RANDOM % $SIZE))
SELECTED_IMAGE=${IMAGES[$INDEX]} 
echo "$SELECTED_IMAGE"
convert "$SELECTED_IMAGE" /tmp/screenshot.png

# blur it
#convert /tmp/screenshot.png -resize 1920x1080 -blur 0x12 /tmp/screenshotblur.png
convert /tmp/screenshot.png -resize 1920x1080 /tmp/screenshotblur.png
rm /tmp/screenshot.png

trap revert HUP INT TERM
xset +dpms dpms 10 10 10
# lock the screen
i3lock -i /tmp/screenshotblur.png -n
revert

# sleep 1 adds a small delay to prevent possible race conditions with suspend
#sleep 10

#xset dpms force off

exit 0
