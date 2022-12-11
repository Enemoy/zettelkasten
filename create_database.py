#!/usr/bin/python

import sqlite3
import bib_file_converter
import os
import main_config as cfg
import zettelkasten_functions as zfn

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

    TABLE_CREATION_COMMAND = "CREATE TABLE " + TABLENAME + """(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                citekey text NOT NULL UNIQUE,
                entrytype text,
                author text,
                title text,
                year text,
                publisher text,
                editor text,
                address text,
                pages text,
                month text,
                booktitle text,
                journal text,
                volume text,
                number text,
                edition text,
                isbn text,
                keywords text,
                doi text,
                url text,
                institution text,
                note text,
                chapter text,
                school text,
                issn text,
                shorthand text,
                type text,
                eprint text,
                crossref text,
                series text,
                addendum text,
                organization text,
                abstract text,
                path_to_bibfile text,
                date text,
                tag_1 text,
                tag_2 text,
                tag_3 text,
                tag_4 text,
                tag_5 text
            )"""

    try:
        c.execute(TABLE_CREATION_COMMAND)
    except sqlite3.OperationalError:
        print("Table already exists:", TABLENAME)

    return

def create_datapoints_table(PATH_TO_DATABASE, TABLENAME):
    # Creates the datapoint table
    conn = sqlite3.connect(PATH_TO_DATABASE)

    c = conn.cursor()

    TABLE_CREATION_COMMAND = "CREATE TABLE "+  TABLENAME + """(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                citekey text,
                page text,
                summary text,
                content_path text,
                tag_1 text,
                tag_2 text,
                tag_3 text,
                tag_4 text,
                tag_5 text,
                date text
            )"""

    try:
        c.execute(TABLE_CREATION_COMMAND)

    except sqlite3.OperationalError:
        print("Table already exists:", TABLENAME)

    return

def create_citations_table(PATH_TO_DATABASE, TABLENAME):
    # Creates the citation table
    conn = sqlite3.connect(PATH_TO_DATABASE)

    c = conn.cursor()

    TABLE_CREATION_COMMAND = "CREATE TABLE " +  TABLENAME + """(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                citekey text,
                page text,
                quote_path text,
                tag_1 text,
                tag_2 text,
                tag_3 text,
                tag_4 text,
                tag_5 text,
                date text
            )"""

    try:
        c.execute(TABLE_CREATION_COMMAND)

    except sqlite3.OperationalError:
        print("Table already exists:", TABLENAME)

    return

def main():
    # if cfg.Str_path_bibfolder.startswith("~"):
    #     DB_PATH = cfg.HOME + cfg.database_file [1:]
    # else:
    #     DB_PATH  = cfg.database_file
    DB_PATH = zfn.correct_home_path(cfg.database_file)

    # All the stepts in the procedures of the database creation are in seperate functions so they can be called from other python scripts

    check_database_existence(DB_PATH)

    create_sources_table(DB_PATH, cfg.database_bib_sources_tablename)
    create_datapoints_table(DB_PATH, cfg.database_datapoints_tablename)
    create_citations_table(DB_PATH, cfg.database_citations_tablename)

    create_datapoint_directory(cfg.Str_path_datapoint_directory, "content")
    create_datapoint_directory(cfg.Str_path_citation_directory, "citation")


if __name__ == "__main__":
    main()
