#!/usr/bin/env bash

# Integrating Setup
# source "$(dirname -- "${BASH_SOURCE[0]}")/../lib/sourcerer.sh"

# Script starts here.

eval `/home/simon/.bin/zettelkasten/main_config.py`

counter_add() {
    arg1=$1
    shift
	if [[ -z $path ]];
	then
		path=$last_cid_file
	fi
	number=$(cat $path)

	# echo $number
	# echo $Org_roam_dir

	grep_result=$(grep -r ":cid $number " $Org_roam_dir)
	if ! [[ -z $grep_result ]];
	then
		((number++))
	fi

	echo -n $number
	echo $number > $path
}

main() { # Function ability
    arg1=$1
    shift
	if [[ -z $path ]];
	then
		path=$last_cid_file
	fi
	sqlite3 $database_file "select max(cid) from $points_tablename;"
	sqlite3 $database_file "select max(cid) from $points_tablename;" > $path
    case "$1" in "$1") $@;; esac
}


help() {
	grep -E '^[[:space:]]*([[:alnum:]_]+[[:space:]]*\(\)|function[[:space:]]+[[:alnum:]_]+)' $0 | sed 's/() {//' | grep "#" | awk  '{ printf "%-15s", $1; for (i=2; i<=NF; i++) printf "%s%s", (i==2?"":" "), $i; printf "\n" }'
}

case "$1" in "$1") $@;; esac

exit 0
