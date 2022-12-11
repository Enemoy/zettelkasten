#!/usr/bin/python

import sqlite3
import string
import random
import pyperclip
import os
import argparse
import main_config as cfg
import zettelkasten_functions as zfn

Str_manual_usage = "Usage"
Str_manual_description = "This script can query the different tables in the database. You always have to pair one column (-c) with one string to search (-s)"
Str_manual_flag_table = "Which table you want to chose. Default: " + cfg.database_bib_sources_tablename
Str_manual_flag_output = "Which column to output."
Str_manual_flag_column = "Which column to query."
Str_manual_flag_string = "Search term you want to query."
Str_manual_flag_inklusive = "Search inklusivly."

DB_PATH = zfn.correct_home_path(cfg.database_file)

def query_database(COLUMN, SEARCH_TERM, OUTPUT, TABLE):
    # Queries the database with the arguments given and returns a list of strings.
    return_list = []
    OUTPUT_TAGS = False
    conn = sqlite3.connect(DB_PATH)

    if OUTPUT == "tags":
        OUTPUT_TAGS = True
        OUTPUT = "tag_1,tag_2,tag_3,tag_4,tag_5"

    if COLUMN == "tags":
        COLUMN = "(tag_1 || tag_2 || tag_3 || tag_4 || tag_5)"


    if COLUMN == "id":
        EXECUTE_COMMAND = "SELECT " + OUTPUT +   " FROM " + TABLE + " WHERE " + COLUMN + " = " + SEARCH_TERM + ";"
    else:
        EXECUTE_COMMAND = "SELECT " + OUTPUT +   " FROM " + TABLE + " WHERE " + COLUMN + " LIKE '%" + SEARCH_TERM + "%';"

    c = conn.cursor()

    try:
        for row in c.execute(EXECUTE_COMMAND):
            if OUTPUT == "path_to_bibfile":
                for e in row[0].split(";"):
                    return_list.append(e)
            elif OUTPUT_TAGS == True:
                s = ""
                for e in row:
                    s += e + " / "

                s = s.strip(" / ")
                return_list.append(s)
            else:
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

    LIST_COLUMNS_CURRENT = zfn.get_column_names(TABLE)
    LIST_COLUMNS_SOURCES = zfn.get_column_names(cfg.database_bib_sources_tablename)

    tmp_list = []
    for column, search_string in zip(LIST_COLUMN, LIST_SEARCHTERM):
        if column in LIST_COLUMNS_CURRENT:
            # look through columns in the table given by user
            tmp_list = query_database(column, search_string, OUTPUT, TABLE)
        else:
            # expand the search to the sources table
            if column in LIST_COLUMNS_SOURCES:
                # output all entries in sources that match the search term and return their citekeys
                for k in query_database(column, search_string, "citekey", cfg.database_bib_sources_tablename):
                    # go through all entries in the table that have refer to that citekey.
                    for o in query_database("citekey", k, OUTPUT, TABLE):
                        tmp_list.append(o)
            else:
                print("The citekey you were looking for does not exist in", TABLE, "or in", cfg.database_bib_sources_tablename)

        if not BOOL_INKLUSIVE:
            for e in tmp_list:
                if e not in return_list:
                    return_list.append(e)
        else:
            compare_list.append(tmp_list)

    # inklusive does not work with query over sources. Fix this

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
    parser.add_argument("-o", "--output", type=str, default="pretty", help=Str_manual_flag_output)
    parser.add_argument("-c", "--column", type=str, action="append", help=Str_manual_flag_column)
    parser.add_argument("-s", "--string", type=str, action="append", help=Str_manual_flag_string)
    parser.add_argument("-i", "--inklusive", action="store_true", help=Str_manual_flag_inklusive)
    args = parser.parse_args()


    # print("inklusive does not work with query over sources. Fix this")

    BOOL_PRINT_PRETTY = False
    STR_OUTPUT_TYPE = args.output

    if args.output == "pretty":
        BOOL_PRINT_PRETTY = True
        STR_OUTPUT_TYPE = "id"

    if args.table:
        TABLE = args.table
    else:
        TABLE = cfg.database_bib_sources_tablename

    if TABLE == "1":
        TABLE = cfg.database_bib_sources_tablename
    elif TABLE == "2":
        TABLE = cfg.database_datapoints_tablename
    elif TABLE == "3":
        TABLE = cfg.database_citations_tablename

    # Todo: if no args.string, print all entries
    if not args.column or not args.string:
        print("You have put search term into the machine!")
        quit()

    for c in args.column:
        output_list = multi_query(TABLE, args.column, args.string, args.inklusive, STR_OUTPUT_TYPE)

    # 1. Make citekey list from matching sources entries
    # 2. Make id list from previous list where citekeys match

    for e in output_list:
        if BOOL_PRINT_PRETTY == True:
            print(zfn.pretty_print(e, TABLE))
            if e != output_list[len(output_list)-1]:
                print("----\n")
        else:
            print(e)


if __name__ == "__main__":
    main()
