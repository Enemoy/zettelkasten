#!/bin/bash

# This script will let the user choose a citekey or title depending on the column name given in $1 and the search string given in $2
# $3 will decide, if the citekey or the title will be put into the clipboard
# EXAMPLE: dmenu_citekey_search.py author "Jacques Derrida" (looks for all entries of sources containing "Jacques Derrida" in the author column)
# If $1 == TERM, then you will just be able to chose a citekey that will then be passed into the clipboard.


eval `/home/simon/.bin/zettelkasten/main_config.py`

# echo $DROPDOWN_MENU

# DROPDOWN_MENU="rofi -theme-str  'window  {width: 50%;}' -w 2 -M fuzzy -dmenu -i"
DROPDOWN_MENU="rofi -dmenu -case-smart"

# echo -e "Yes\nNo\nMaybe" | $DROPDOWN_MENU

# exit 0

if [[ "${database_file:0:1}" == "~" ]];
then
	database_file="$HOME${database_file:1}"
fi

# This if statement checks, if the input file is a .tex file and tries to find the .bib-file in it in the database.
if [[ "${3: -4}" == ".tex" ]] && [[ "$2" == "path_to_bibfile" ]];
then
	STRING=$(grep \addbibresource $3)

	STRING=${STRING#*\{}
	STRING=${STRING::-1}

	COLUMN=$2
else
	COLUMN=$2
	STRING=$3
fi

if [[ -z $1 ]] || [[ "$1" == "citekey" ]] || [[ "$1" == "TERM" ]];
then
	AWK_FIELD="\$1"
	PROMPT_FIELD="citekey"

elif [[ "$1" == "title" ]];
then
	AWK_FIELD="\$1=\$2=\"\"; print \$0"
	PROMPT_FIELD="title"

fi

if [[ -z $COLUMN ]] && [[ -z $STRING ]];
then
	# echo "No arguments given, showing all sources!"
	output_citekey=$(sqlite3 $database_file "select citekey,title from $database_bib_sources_tablename;" | awk -F '|' '{printf "%30s - ", $1; printf "%s\n", $2}' | $DROPDOWN_MENU -p "Choose $PROMPT_FIELD:" | awk "{printf $AWK_FIELD}"  |  xargs)
	if [[ "$1" == "TERM" ]];
	then
		echo -n $output_citekey
	else
		echo $output_citekey | wl-copy -n
	fi
	# output_citekey=$(sqlite3 $database_file "select citekey,title from $database_bib_sources_tablename;" | awk -F '|' '{printf "%30s - ", $1; printf "%s\n", $2}' | $DROPDOWN_MENU -p "Choose $PROMPT_FIELD:" | awk "{printf $AWK_FIELD}"  |  xargs) | wl-copy -n
else
	sqlite3 $database_file "select citekey,title from $database_bib_sources_tablename where $COLUMN like '%$STRING%';" | awk -F '|' '{printf "%30s - ", $1; printf "%s\n", $2}' | $DROPDOWN_MENU -p "Choose $PROMPT_FIELD:" | awk "{printf $AWK_FIELD}"  | xargs |  wl-copy -n
	# output_citekey=$(sqlite3 $database_file "select citekey,title from $database_bib_sources_tablename where $COLUMN like '%$STRING%';" | awk -F '|' '{printf "%30s - ", $1; printf "%s\n", $2}' | $DROPDOWN_MENU -p "Choose $PROMPT_FIELD:" | awk "{printf $AWK_FIELD}"  | xargs)
fi

# if [[ "$1" == "TERM" ]];
# then
# 	echo $output_citekey
# else
# 	echo $output_citekey | wl-copy -n
# fi

exit 0
