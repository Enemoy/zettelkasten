#!/usr/bin/python

import sqlite3
import string
import random
import pyperclip
import os
import argparse
import main_config as cfg

Str_manual_usage = "Usage"
Str_manual_description = "This script can query the different tables in the database."
Str_manual_flag_table = "Which table you want to chose."
Str_manual_flag_output = "Which column to output."
Str_manual_flag_column = "Which column to query."
Str_manual_flag_string = "Search term you want to query."
Str_manual_flag_inklusive = "Search inklusivly."

DB_PATH = cfg.HOME + cfg.database_file[1:]

def query_database(COLUMN, SEARCH_TERM, OUTPUT, TABLE):
    # Queries the database with the arguments given and returns a list of strings.
    return_list = []
    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()

    EXECUTE_COMMAND = "SELECT " + OUTPUT +   " FROM " + TABLE + " WHERE " + COLUMN + " LIKE '%" + SEARCH_TERM + "%';"

    try:
        for row in c.execute(EXECUTE_COMMAND):
            return_list.append(row[0])
    except sqlite3.OperationalError:
        print("SQL Error: The column or table you chose doesn't exist!")
        quit()

    return return_list

def multi_query(TABLE, LIST_COLUMN, LIST_SEARCHTERM, BOOL_INKLUSIVE=False, OUTPUT="citekey"):

    if LIST_COLUMN == None or LIST_SEARCHTERM == None:
        print("You have to provide more arguments!")
        quit()

    if len(LIST_COLUMN) != len(LIST_SEARCHTERM):
        print("The amount of columns and strings have to be the same!")
        quit()

    if len(LIST_COLUMN) == 1:
        #print("Ignoring inklusive flag as you only provided one search term!")
        BOOL_INKLUSIVE = False

    # List of entries to be output
    return_list = []

    # List of lists to compare if all results are in all lists
    compare_list = []

    for column, search_string in zip(LIST_COLUMN, LIST_SEARCHTERM):
        tmp_list = query_database(column, search_string, OUTPUT, TABLE)
        if not BOOL_INKLUSIVE:
            for e in tmp_list:
                if e not in return_list:
                    return_list.append(e)
        else:
            compare_list.append(tmp_list)


    if BOOL_INKLUSIVE:
        compare_list_base = compare_list[0]
        compare_list_rest = compare_list[1:]

        # Compares the first list with results to all the others and if the value is in all the others, it will add it to the output list.
        for r in compare_list_base:
            for l in compare_list_rest:
                if r in l:
                    return_list.append(r)
                else:
                    try:
                        return_list.remove(r)
                    except ValueError:
                        1 == 1

    return return_list


def main():
    # Set up the argument input
    parser = argparse.ArgumentParser(description=Str_manual_description, usage=Str_manual_usage, add_help=True)
    parser.add_argument("-t", "--table", type=str, help=Str_manual_flag_table)
    parser.add_argument("-o", "--output", type=str, help=Str_manual_flag_output)
    parser.add_argument("-c", "--column", type=str, action="append", help=Str_manual_flag_column)
    parser.add_argument("-s", "--string", type=str, action="append", help=Str_manual_flag_string)
    parser.add_argument("-i", "--inklusive", action="store_true", help=Str_manual_flag_inklusive)
    args = parser.parse_args()

    if args.table:
        TABLE = args.table
    else:
        print("No table given!")
        quit()

    if not args.column or not args.string:
        print("You have put search term into the machine!")
        quit()


    if args.output == None:
        output_list = multi_query(TABLE, args.column, args.string, args.inklusive)
    else:
        output_list = multi_query(TABLE, args.column, args.string, args.inklusive, args.output)

    for e in output_list:
        print(e)


    quit()


if __name__ == "__main__":
    main()
