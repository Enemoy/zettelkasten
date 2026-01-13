#!/usr/bin/python

import sqlite3
import bib_file_converter
import os
import argparse
import sys

sys.path.insert(0, '/home/simon/.bin/zettelkasten/')
import main_config as cfg
import zettelkasten_functions as zfn

Str_manual_description="This script will create the database, the tables inside it and the content folders for quotes and datapoints. The variables are stored in the config file."
Str_manual_usage="zettelkasten create [-h/--help]"

# Creates the database and the three different tables in it.
# If the table already exists, it won't be created.

def create_datapoint_directory(PATH, NAME):
    # Create folder for datapoint_collection contents
    # Create path from config file
    # if PATH.startswith("~"):
    #     PATH = cfg.HOME + PATH[1:]
    PATH = zfn.correct_home_path(PATH)


    if not os.path.exists(PATH):
        os.makedirs(PATH)
        print("Creating", NAME, "directory for datapoint table:", PATH)
    else:
        print(NAME, "directory already exists!")

    return

def check_database_existence(PATH_TO_DATABASE):
    # Create database path
    DB_EXISTS = os.path.exists(PATH_TO_DATABASE)

    if DB_EXISTS == True:
        print("Database exists in file:", cfg.database_file, "\nNew database won't be created!")
    else:
        print("Creating Database!")


def create_sources_table(PATH_TO_DATABASE, TABLENAME):
    # creates the sources table
    conn = sqlite3.connect(PATH_TO_DATABASE)

    c = conn.cursor()

    # Is display really needed or can note just be used?
    TABLE_CREATION_COMMAND = "CREATE TABLE " + TABLENAME + """ (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                `citekey` text NOT NULL UNIQUE DEFAULT '',
                `type` text DEFAULT '',
                `display` text DEFAULT '',
                `entrytype` text DEFAULT '',
                `author` text DEFAULT '',
                `title` text DEFAULT '',
                `year` text DEFAULT '',
                `publisher` text DEFAULT '',
                `editor` text DEFAULT '',
                `address` text DEFAULT '',
                `pages` text DEFAULT '',
                `month` text DEFAULT '',
                `booktitle` text DEFAULT '',
                `journal` text DEFAULT '',
                `volume` text DEFAULT '',
                `number` text DEFAULT '',
                `subtitle` text DEFAULT '',
                `edition` text DEFAULT '',
                `isbn` text DEFAULT '',
                `keywords` text DEFAULT '',
                `doi` text DEFAULT '',
                `url` text DEFAULT '',
                `institution` text DEFAULT '',
                `note` text DEFAULT '',
                `chapter` text DEFAULT '',
                `school` text DEFAULT '',
                `issn` text DEFAULT '',
                `origdate` text DEFAULT '',
                `shorthand` text DEFAULT '',
                `eprint` text DEFAULT '',
                `crossref` text DEFAULT '',
                `series` text DEFAULT '',
                `addendum` text DEFAULT '',
                `organization` text DEFAULT '',
                `abstract` text DEFAULT '',
                `file` text DEFAULT '',
                `tags` text DEFAULT '',
                `date` text DEFAULT ''
            )"""

    # c.execute(TABLE_CREATION_COMMAND)
    try:
        c.execute(TABLE_CREATION_COMMAND)
    except sqlite3.OperationalError:
        print("SQL-Error or: Table already exists:", TABLENAME)

    return

def create_datapoints_table(PATH_TO_DATABASE, TABLENAME):
    # Creates the datapoint table
    conn = sqlite3.connect(PATH_TO_DATABASE)

    c = conn.cursor()

    TABLE_CREATION_COMMAND = "CREATE TABLE "+  TABLENAME + """(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                `type` text,
                `citekey` text,
                `page` text,
                `file` text,
                `note` text DEFAULT '',
                `content` text DEFAULT ''
            )"""

    # c.execute(TABLE_CREATION_COMMAND)
    try:
        c.execute(TABLE_CREATION_COMMAND)

    except sqlite3.OperationalError:
        print("Table already exists:", TABLENAME, "(or there is some other exception, this is just an educated guess.")

    return

def create_citations_table(PATH_TO_DATABASE, TABLENAME):
    # Creates the citation table
    conn = sqlite3.connect(PATH_TO_DATABASE)

    c = conn.cursor()

    TABLE_CREATION_COMMAND = "CREATE TABLE " +  TABLENAME + """(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                citekey text,
                page text,
                path text,
                tag_1 text,
                tag_2 text,
                tag_3 text,
                tag_4 text,
                tag_5 text,
                date text
            )"""

    c.execute(TABLE_CREATION_COMMAND)
    try:
        c.execute(TABLE_CREATION_COMMAND)

    except sqlite3.OperationalError:
        print("Table already exists:", TABLENAME)

    return

def main():
    parser = argparse.ArgumentParser(description=Str_manual_description, usage=Str_manual_usage, add_help=True)
    args = parser.parse_args()

    DB_PATH = zfn.correct_home_path(cfg.database_file)

    # All the stepts in the procedures of the database creation are in seperate functions so they can be called from other python scripts

    check_database_existence(DB_PATH)

    create_sources_table(DB_PATH, cfg.database_bib_sources_tablename)
    create_datapoints_table(DB_PATH, cfg.points_tablename)
    # create_citations_table(DB_PATH, cfg.database_citations_tablename)

    create_datapoint_directory(cfg.Str_path_datapoint_directory, "content")
    create_datapoint_directory(cfg.Str_path_citation_directory, "citation")


if __name__ == "__main__":
    main()
