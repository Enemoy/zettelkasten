#!/usr/bin/python

import sqlite3
import string
import random
import pyperclip
import os
import argparse
import main_config as cfg

Str_manual_usage = "change_citekeys_all.py -o [old citekey] -n [new citekey]"
Str_manual_description = "This script will change all old citekeys to new citekeys."
Str_manual_flag_table = "Which table you want to chose. Default: all."
Str_manual_flag_old = "The current / old citekey, you want to change."
Str_manual_flag_new = "The citekey you want the old one to change to."

if cfg.database_file.startswith("~"):
    DB_PATH = cfg.HOME + cfg.database_file [1:]
else:
    DB_PATH  = cfg.database_file

# This script will give the user the possibility to change a citekey-value in datapoints and citations throughout the whole tables.
# This is usefull when a citekey is changed in the .bib-files that get converted into the database and there used to be references to this citekey.

def execute_sql_command(input_command, database = DB_PATH):
    # executes the sql-command onto the database

    print(database)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute(input_command)

    conn.commit()

    return

def change_citekey(STR_CITEKEY_OLD, STR_CITEKEY_NEW, TABLENAME="all"):
    print(STR_CITEKEY_OLD)
    print(STR_CITEKEY_NEW)

    list_input_table_options = ["all", cfg.database_datapoints_tablename, cfg.database_citations_tablename]

    print(list_input_table_options)

    if TABLENAME not in list_input_table_options:
        print("You have to choose a exisiting table or input all!")
        quit()

    if TABLENAME == "all":
        #Execute command for both tables
        EXECUTE_COMMAND = "UPDATE " + cfg.database_datapoints_tablename  + " SET citekey = '" + STR_CITEKEY_NEW + "' WHERE citekey = '" + STR_CITEKEY_OLD + "';"
        execute_sql_command(EXECUTE_COMMAND)

        EXECUTE_COMMAND = "UPDATE " + cfg.database_citations_tablename + " SET citekey = '" + STR_CITEKEY_NEW + "' WHERE citekey = '" + STR_CITEKEY_OLD + "';"
        execute_sql_command(EXECUTE_COMMAND)
    else:
        EXECUTE_COMMAND = "UPDATE " + TABLENAME + " SET citekey = '" + STR_CITEKEY_NEW + "' WHERE citekey = '" + STR_CITEKEY_OLD + "';"
        execute_sql_command(EXECUTE_COMMAND)

    return

def main():
    list_table_input_choices = [cfg.database_citations_tablename, cfg.database_datapoints_tablename, "all"]
    parser = argparse.ArgumentParser(description=Str_manual_description, usage=Str_manual_usage, add_help=True)
    parser.add_argument("-o", "--old_citekey", required=True, type=str, help=Str_manual_flag_old)
    parser.add_argument("-n", "--new_citekey", required=True, type=str, help=Str_manual_flag_new)
    parser.add_argument("-t", "--table", required=False, type=str, help=Str_manual_flag_table, choices = list_table_input_choices, default = "all")
    args = parser.parse_args()

    change_citekey(args.old_citekey, args.new_citekey, args.table)

if __name__ == "__main__":
    main()
