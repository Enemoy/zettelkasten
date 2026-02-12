#!/usr/bin/python

import sqlite3
import string
import random
import pyperclip
import os
import argparse
import sys

sys.path.insert(0, '/home/simon/.bin/zettelkasten/')

import main_config as cfg
import zettelkasten_functions as zfn

Str_manual_usage = "zettelkasten query -t [TABLE] -c [COLUMN] -s [STRING] -o [OUTPUT]"
Str_manual_description = "This script can query the different tables in the database. You always have to pair one column (-c) with one string to search (-s)"
Str_manual_flag_table = "Which table you want to chose. Default: " + cfg.database_bib_sources_tablename
Str_manual_flag_output = "Which column to output."
Str_manual_flag_column = "Which column to query."
Str_manual_flag_string = "Search term you want to query. If column is \"id\", you can input \"last\" to print the last entry added to the table. If you put STDIN as  a string, the programm will take the argument from standard input. If there are multiple occurences of STDIN, the programm will loop through the lines of input."
Str_manual_flag_inklusive = "Search inklusivly."

DB_PATH = zfn.correct_home_path(cfg.database_file)

def query_database(column_list, search_list, output, table = 1):

    return_list = []

    if len(column_list) == len(search_list):
        query_dict = dict(zip(column_list, search_list))
    else:
        print("The amount of columns and search terms are not the same, stopping!")
        quit()

    query_all_bool = False

    if "all" in column_list:
        query_all_bool = True

    results = zfn.db_select_query(table, query_dict, query_all_bool)

    table=int(table)

    for i in results:
        if output == "pretty":
            # print(zfn.pretty_format_citation(i))
            if table ==  1:
                return_list.append(zfn.pretty_format_source(i))
            else:
                return_list.append(zfn.pretty_format_citation(i))
        elif output == "org":
            if table ==  1:
                return_list.append(zfn.org_format_source(i))
            else:
                return_list.append(zfn.org_format_citation(i))
        else:
            try:
                return_list.append(i[zfn.key_conversion(output, table)])
            except KeyError as e:
                print(e)
                print("You probably chose the wrong column.")
                quit()

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

    if args.table == None:
        args.table = 1


    output_list = query_database(args.column, args.string, args.output, args.table)

    # print(len(output_list))
    for i in output_list:
        if i != "":
            print(i)

    return



if __name__ == "__main__":
    main()
