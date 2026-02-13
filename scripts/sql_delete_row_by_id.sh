#!/bin/bash

# This short script will delete a row by sid or cid in the fitting table.
# Table > 1 → citations / datapoints get deleted, otherwise it's a source.

eval `/home/simon/.bin/zettelkasten/main_config.py`

echo "Deleting entry, careful!"; read -p "Please enter the cid / sid: " id; read -p "Please enter the table: " table_id; if [[ $table == 1 ]]; then table="sources_collection"; sid_or_cid="sid"; else table="points_collection"; sid_or_cid="cid"; fi; sqlite3 $database_file "DELETE FROM $table WHERE $sid_or_cid = $id;"
