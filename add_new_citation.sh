#!/bin/bash

# This script will copy the form for a new datapoint to a tmp file, let's you edit the tmp file and parses the content on to a python script.
# Last argument has to be the path
eval `/home/simon/.bin/zettelkasten/main_config.py`

TMP_FILENAME_1=$(echo $RANDOM | md5sum | head -c 20)
TMP_FILENAME_2=$(echo $RANDOM | md5sum | head -c 20)

TMP_FILEPATH_1="/tmp/${TMP_FILENAME_1}"
TMP_FILEPATH_2="/tmp/${TMP_FILENAME_2}"

if [[ "${CITATION_FORM_PATH:0:1}" == "~" ]];
then
	CITATION_FORM_PATH="$HOME${CITATION_FORM_PATH:1}"
fi

cp "$CITATION_FORM_PATH" $TMP_FILEPATH_1

help_function(){
	# This is the help for the script
	echo "This script provides different ways to add a new citation to the database."
	echo "The first argument has to be -l (to make the edits in the local terminal) or -t (to edit in zenity and a popup-terminal)"
	echo "The second argument is either a path to a file containing the citation, -c (to copy the citation from the local clipboard) or nothing to manually enter the citation in a terminal."
}

open_terminal(){
	FORM_DATA=$(zenity --forms --width=500 --title="Citation information" \
		--text="Please enter the data for your citation entry." \
		--add-entry="Citekey"  \
		--add-entry="Page" \
		--add-entry="Tag 1" \
		--add-entry="Tag 2" \
		--add-entry="Tag 3" \
		--add-entry="Tag 4" \
		--add-entry="Tag 5" )

	# extract variables from zenity input.
	CITEKEY=$(echo $FORM_DATA | awk -F '|' '{printf $1}')
	PAGE=$(echo $FORM_DATA | awk -F '|' '{printf $2}')
	TAG_1=$(echo $FORM_DATA | awk -F '|' '{printf $3}')
	TAG_2=$(echo $FORM_DATA | awk -F '|' '{printf $4}')
	TAG_3=$(echo $FORM_DATA | awk -F '|' '{printf $5}')
	TAG_4=$(echo $FORM_DATA | awk -F '|' '{printf $6}')
	TAG_5=$(echo $FORM_DATA | awk -F '|' '{printf $7}')

	TAG_LIST="$TAG_1,$TAG_2,$TAG_3,$TAG_4,$TAG_5"

	sed -i "s|CITEKEY=|CITEKEY=$CITEKEY|g" $TMP_FILEPATH_1
	sed -i "s|PAGE=|PAGE=$PAGE|g" $TMP_FILEPATH_1
	sed -i "s|TAGS=|TAGS=$TAG_LIST|g" $TMP_FILEPATH_1

	# Procedure for adding a new datapoint in zenity form and a popup terminal
	if [[ $1 == "-c" ]];
	then
		# Adding the citation from the system clipboard
		#$POPUP_TERMINAL  -e $EDITOR $TMP_FILEPATH_1
		python ~/.bin/zettelkasten/add_new_datapoint.py -d -c -p $TMP_FILEPATH_1
	elif [[ $1 == "manual" ]];
	then
		# Adding the citation through vim
		echo "<Write the content of your datapoint into this file, safe and quit.>" > $TMP_FILEPATH_2
		echo $TMP_FILEPATH_2
		sed -i "s|QUOTE=|QUOTE=$TMP_FILEPATH_2|g" $TMP_FILEPATH_1
		$POPUP_TERMINAL -e $EDITOR $TMP_FILEPATH_2
		#$POPUP_TERMINAL -e $EDITOR $TMP_FILEPATH_1
		python ~/.bin/zettelkasten/add_new_datapoint.py -d -p $TMP_FILEPATH_1
		rm $TMP_FILEPATH_2
	else
		# Adding the citation from a textfile
		sed -i "s|QUOTE=|QUOTE=$1|g" $TMP_FILEPATH_1
		#$POPUP_TERMINAL -e $EDITOR $TMP_FILEPATH_1
		python ~/.bin/zettelkasten/add_new_datapoint.py -d -p $TMP_FILEPATH_1
	fi
}

open_local(){
	# Procedure for adding a new citation in the local terminal
	if [[ $1 == "-c" ]];
	then
		# Adding the citation from the system clipboard
		$EDITOR $TMP_FILEPATH_1
		python ~/.bin/zettelkasten/add_new_datapoint.py -d -c -p $TMP_FILEPATH_1
	elif [[ $1 == "manual" ]];
	then
		# Adding the content through vim
		echo "<Write the content of your datapoint into this file, safe and quit.>" > $TMP_FILEPATH_2
		#echo $TMP_FILEPATH_2
		sed -i "s|QUOTE=|QUOTE=$TMP_FILEPATH_2|g" $TMP_FILEPATH_1
		$EDITOR $TMP_FILEPATH_2
		$EDITOR $TMP_FILEPATH_1
		python ~/.bin/zettelkasten/add_new_datapoint.py -d -p $TMP_FILEPATH_1
		rm $TMP_FILEPATH_2
	else
		# Adding the content from a textfile
		sed -i "s|QUOTE=|QUOTE=$1|g" $TMP_FILEPATH_1
		$EDITOR $TMP_FILEPATH_1
		python ~/.bin/zettelkasten/add_new_datapoint.py -d -p $TMP_FILEPATH_1
	fi
}

case $1 in
	-t | --terminal)
		LOCAL=0
		;;

	-l | --local)
		LOCAL=1
		;;

	-h | --help)
		help_function
		exit 0
		;;

	*)
		echo "Wrong first argument."
		exit 0
		;;

esac

shift

if [[ -z $1 ]];
then
	CONTENT_TYPE="manual"
else
	CONTENT_TYPE=$1
fi

if [[ $LOCAL == "1" ]];
then
	open_local $CONTENT_TYPE
else
	open_terminal $CONTENT_TYPE
fi

rm $TMP_FILEPATH_1

exit 0
