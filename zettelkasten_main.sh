#!/bin/bash

# This script will handle the user interface with the zettelkasten.
# It works by looking at the first argument, chosing the right script and
# then passing on the other arguments to the corresponding python script.
# It's basically one big case statement.

eval `/home/simon/.bin/zettelkasten/main_config.py`

case $1 in

	query | search | find)
		#echo "Query"
		shift
		${Str_path_sourcecode}query_database_v2.py  "$@"
		;;

	compile)
		#echo "bibfile converter"
		shift
		# ${Str_path_sourcecode}bib_file_converter.py  "$@"
		${Str_path_sourcecode}populate_database.py
		;;

	bibfile)
		# echo "compiling main bib-file"
		shift
		${Str_path_sourcecode}create_bibfiles_from_db.py  "$@"
		;;

	backup)
		#echo "backup"
		shift
		${Str_path_sourcecode}backup_files.py  "$@"
		;;

	create | setup)
		#echo "creating database"
		shift
		${Str_path_sourcecode}create_database.py  "$@"
		;;

	edit)
		#echo "Editing entry"
		shift
		${Str_path_sourcecode}edit_entry.py  "$@"
		;;

	convert)
		#echo "Editing entry"
		shift
		bash ${Str_path_sourcecode}dmenu_convert_to_org_clip.sh
		;;

	citekey)
		#echo "looking through citekeys with dmenu"
		shift
		${Str_path_sourcecode}dmenu_citekey_search.sh  "$@"
		;;

	delete)
		#echo "deleting rows"
		shift
		${Str_path_sourcecode}delete_rows.py  "$@"
		;;

	check)
		#echo "Checking if citekeys exisit"
		shift
		${Str_path_sourcecode}check_citekeys_existing.py  "$@"
		;;

	change)
		#echo "changing all citekeys in a table"
		shift
		${Str_path_sourcecode}change_citekeys_all.py  "$@"
		;;

	citation)
		#echo "adding new citation"
		shift
		${Str_path_sourcecode}add_new_citation.sh  "$@"
		;;

	datapoint)
		#echo "adding new datapoint"
		shift
		${Str_path_sourcecode}add_new_datapoint.sh  "$@"
		;;

	config)
		#echo "editing the config file"
		shift
		$EDITOR ${Str_path_sourcecode}main_config.py
		;;

	bibfile)
		#echo "Choosing a bibfile"
		shift
		${Str_path_sourcecode}dmenu_bibfliles.sh  "$@"
		;;

	au)
		shift
		${Str_path_sourcecode}query_database_v2.py -c author -s "$@"
		;;

	ti)
		shift
		${Str_path_sourcecode}query_database_v2.py -c title -s "$@"
		;;

	ci)
		shift
		${Str_path_sourcecode}query_database_v2.py -c citekey -s "$@"
		;;

	ye)
		shift
		${Str_path_sourcecode}query_database_v2.py -c citekey -s "$@"
		;;

	nb)
		shift
		${Str_path_sourcecode}query_database_v2.py -c id -s "$@"
		;;
	ta | tag)
		shift
		${Str_path_sourcecode}query_database_v2.py -c tags -s "$@"
		;;


	help | -h | --help)
		echo -e "Options: \n\tquery\n\tconvert\n\tcomplete\n\tbackup\n\tcreate\n\tedit\n\tcitekey\n\tdelete\n\tcheck\n\tchange\n\tcitation\n\tdatapoint\n\tbibfile\n\tconfig"
		echo -e "Choose one of these options!\nIf you want more usage information, add the --help / -h flag after the first argument."
		;;

	*)
		echo "Out of all the options to choose the one you picked is invalid."
		;;

esac

exit 0
