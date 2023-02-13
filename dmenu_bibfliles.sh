#!/bin/bash

#This script will look for the bibliographies available in the according folder and give an option to choose one to copy to the clipboard.

eval `/home/simon/.bin/zettelkasten/main_config.py`

#MENU="rofi -dmenu"

if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]];
then
	echo "This script will allow you to choose a bibfile with dmenu or rofi."
	echo "The -c flag will copy the name of the bibfile to the clipboard. The -h flag will display this help."
	exit 0
fi

TITLE=$(find $Str_path_bibfolder -type f -name "*.bib" |  cut -d'/' -f11- | $DROPDOWN_MENU -p "Choose bibfile")
TITLE="${TITLE#*\/}"

if [[ "$1" == "-c" ]];
then
	echo -n $TITLE | xclip -selection "clipboard"
else
	echo $(find $Str_path_bibfolder -type f -name $TITLE)
fi

exit 0
