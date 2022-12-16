#/bin/bash

#This script will look for the bibliographies available in the according folder and give an option to choose one to copy to the clipboard.

eval `/home/simon/.bin/zettelkasten/main_config.py`

#MENU="rofi -dmenu"

TITLE=$(find $Str_path_bibfolder -type f -name "*.bib" |  cut -d'/' -f11- | $DROPDOWN_MENU -p "Choose bibfile")
TITLE="${TITLE#*\/}"

if [[ "$1" == "-c" ]];
then
	echo -n $TITLE | xclip -selection "clipboard"
else
	echo $(find $Str_path_bibfolder -type f -name $TITLE)
fi

exit 0
