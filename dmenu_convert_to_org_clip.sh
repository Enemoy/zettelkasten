#!/bin/bash

# Gives the files in a directory to dmenu and converts the content to org source

eval `/home/simon/.bin/zettelkasten/main_config.py`

DROPDOWN_MENU="rofi -dmenu -case-smart"

target_dir="$HOME/Downloads/"

# text=$(cat $target_dir$(find $target_dir -type f  -printf "%P\n" | $DROPDOWN_MENU))
text="$target_dir$(find $target_dir -type f  -printf "%P\n" | $DROPDOWN_MENU)"

text=$(python3 convert_bib_to_org_handler.py $text)

if [[ -z "$text" ]];
then
	echo "Conversion didn't work, text is empty!"
else
	echo "$text" | wl-copy
fi

exit 0
