#!/bin/bash

# This script will let the user choose a citekey depending on the column name given in $1 and the search string given in $2
# EXAMPLE: dmenu_citekey_search.py author "Jacques Derrida" (looks for all entries of sources containing "Jacques Derrida" in the author column.

eval `/home/simon/.bin/zettelkasten/main_config.py`

if [[ "${database_file:0:1}" == "~" ]];
then
	database_file="$HOME${database_file:1}"
fi

if [[ -z $1 ]] && [[ -z $2 ]];
then
	echo "No arguments given, showing all sources!"
	sqlite3 $database_file "select citekey,title from $database_bib_sources_tablename;" | awk -F '|' '{printf "%30s - ", $1; printf "%s\n", $2}' | $DROPDOWN_MENU -p "Choose citekey:" | awk '{printf $1}'  | tr -d '()' | xclip -selection "clipboard"
else
	sqlite3 $database_file "select citekey,title from $database_bib_sources_tablename where $1 like \"%$2%\";" | awk -F '|' '{printf "%30s - ", $1; printf "%s\n", $2}' | $DROPDOWN_MENU -p "Choose citekey:" | awk '{printf $1}'  | tr -d '()' | xclip -selection "clipboard"
fi

exit 0
