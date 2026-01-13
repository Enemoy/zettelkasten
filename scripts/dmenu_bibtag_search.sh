#!/bin/bash

# This script will let the user choose a tag from the database.


eval `/home/simon/.bin/zettelkasten/main_config.py`

# DROPDOWN_MENU="rofi -dmenu -case-smart"

tag=$(sqlite3 $database_file "select tags from $database_bib_sources_tablename;" | tr , "\n" | sed '/^$/d'  | sed 's/^[[:space:]]*//' | sed -e 's/\ *$//g' | sort -f | uniq -i | $DROPDOWN_MENU)

if [[ ! -z $tag ]];
then
	wl-copy $tag
fi

exit 0
