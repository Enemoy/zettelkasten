#!/usr/bin/python

import sqlite3
import bib_file_converter
import os
import argparse
import subprocess
import main_config as cfg


# This function edits specific entries in datapoints or citations.
# If the content will be edited, instead of editing the path, the system editor will be used.

Str_flag_table="Choose the table in which you want to edit an entry."
Str_flag_id="Choose the id of the entry you want to edit."
Str_flag_column="The column you want to edit."
Str_flag_entry="The new value the column should have (will be ignored if the content is edited"
Str_manual_description="This script changes the column value of an entry in a specific table."
Str_manual_usage="Usage"

list_table_choices = [cfg.database_datapoints_tablename, cfg.database_citations_tablename]

if cfg.database_file.startswith("~"):
    DB_PATH = cfg.HOME + cfg.database_file [1:]
else:
    DB_PATH  = cfg.database_file

def execute_sql_command(input_command, database = DB_PATH):
    # executes the sql-command onto the database

    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()

    except sqlite3.OperationalError:
        print("SQL OperationalError. You probably chose a wrong column!")

    c.execute(input_command)

    conn.commit()

    return

def change_textfile_content(input_command, database=DB_PATH):
    # This function extracts the file path to edit and creates a bash command to make editing in the system editor possible.

    conn = sqlite3.connect(database)
    c = conn.cursor()

    PATH = ""
    try:
        for row in c.execute(input_command):
            PATH = row[0]

    except sqlite3.OperationalError:
        print("SQL OperationalError. You probably chose a wrong column!")
        quit()

    conn.commit()

    if PATH != "":
        EDITOR = os.environ.get('EDITOR', 'vim')
        subprocess.call([EDITOR, PATH])

    return

def change_entry(TABLENAME, ID, COLUMN, NEW_VALUE):

    if NEW_VALUE == None:
        EXECUTE_COMMAND = "SELECT " + COLUMN + " FROM " + TABLENAME + " WHERE id = " + str(ID) + ";"
        change_textfile_content(EXECUTE_COMMAND)
    else:
        EXECUTE_COMMAND = "UPDATE " + TABLENAME + " SET " + COLUMN + " = '" + NEW_VALUE + "' WHERE id = " + str(ID) + ";"
        execute_sql_command(EXECUTE_COMMAND)

    return

def main():
    parser = argparse.ArgumentParser(description=Str_manual_description, usage=Str_manual_usage, add_help=True)
    parser.add_argument("-t", "--table", type=str, default=cfg.database_datapoints_tablename, choices = list_table_choices , help=Str_flag_table)
    parser.add_argument("-i", "--id", type=int, required=True, help=Str_flag_id)
    parser.add_argument("-c", "--column", type=str, required=True, help=Str_flag_column)
    parser.add_argument("-n", "--new_value", type=str, help=Str_flag_entry)
    args = parser.parse_args()

    list_content_edit_options = ["content_path", "quote_path", "path"]

    if args.column not in list_content_edit_options:
        if args.new_value == None:
            print("You have to input a -n argument if you choose this column.")
            quit()

    if args.column == "path":
        if args.table == cfg.database_datapoints_tablename:
            COLUMN = "content_path"
        if args.table == cfg.database_citations_tablename:
            COLUMN = "quote_path"
    else:
        COLUMN = args.column

    change_entry(args.table, args.id, COLUMN, args.new_value)


if __name__ == "__main__":
    main()
