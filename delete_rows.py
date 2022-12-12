#!/usr/bin/python

import os
import sqlite3
import argparse
import shutil
import main_config as cfg
import zettelkasten_functions as zfn


Str_manual_usage = "Usage: ./delete_rows.py -t [TABLE] -i [ID]"
Str_manual_description = "This script will delete the row with the id you have given as an argument from " + cfg.database_datapoints_tablename + " or " + cfg.database_citations_tablename + "."
Str_manual_flag_table = "Which table you want to chose. Default: " + cfg.database_datapoints_tablename
Str_manual_flag_id = "The id of the entry you want to delete."

list_table_options = ["2", "3", cfg.database_datapoints_tablename, cfg.database_citations_tablename]

def main():
    # Set up the argument input
    parser = argparse.ArgumentParser(description=Str_manual_description, usage=Str_manual_usage, add_help=True)
    parser.add_argument("-t", "--table", type=str, choices=list_table_options, default=cfg.database_datapoints_tablename, help=Str_manual_flag_table)
    parser.add_argument("-i", "--id", action="store", type=int, required=True, help=Str_manual_flag_id)
    args = parser.parse_args()

    if args.table == "2":
        TABLE = cfg.database_datapoints_tablename
    elif args.table == "3":
        TABLE = cfg.database_citations_tablename
    else:
        TABLE = args.table

    zfn.delete_row(args.id, TABLE)

    return


if __name__ == "__main__":
    main()
