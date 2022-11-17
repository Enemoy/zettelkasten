#!/usr/bin/python

import sqlite3
import string
import random
import pyperclip
import os
import argparse
import main_config as cfg

# This script will make accessing data from the database easier (e.g. with bash scripts, dmenu etc)

Str_manual_description="This script will print different contents of the database."
Str_manual_usage="extract_database_infos.py [args]"
Str_manual_flag_file="Choose this option if the content of the information is stored in a textfile."

def extract_single_column(LIST_COLUMN, LIST_STRING, BOOL_EXCLUSIVE=False):
    for row in c.execute("SELECT title,author,path_to_bibfile FROM sources_collection;"):
        print(row[0])

def main():
    # Set up the argument input
    parser = argparse.ArgumentParser(description=Str_manual_description, usage=Str_manual_usage, add_help=True)
    parser.add_argument("-t", "--table", type=str, help=Str_manual_flag_file)
    parser.add_argument("-c", "--column", type=str, action="append", help=Str_manual_flag_file)
    parser.add_argument("-s", "--string", type=str, action="append", help=Str_manual_flag_file)
    args = parser.parse_args()

    if not args.table:
        print("You have to specify a table with -t!")
        print("Available tables are:\n\t", cfg.database_bib_sources_tablename, cfg.database_datapoints_tablename, cfg.database_citations_tablename)
        quit()

    if not args.column:
        print("You have to specify at least one column with -c!")
        quit()

    if args.string:
        for s in args.string:
            extract_single_column(string)
    else:
        extract_single_column(input_column, "ALL_CONTENTS")

if __name__ == "__main__":
    main()
