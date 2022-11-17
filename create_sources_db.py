#!/usr/bin/python

import sqlite3
import bib_file_converter
import os
import main_config as cfg

# Creates the database and the three different tables in it.
# If the table already exists, it won't be created.

# DB_PATH = 'bib_sources.db'
DB_PATH = cfg.database_file.split("/")[-1]
HOME = os.path.expanduser( '~' )

def create_content_directory(PATH, NAME):
    # Create folder for datapoint_collection contents
    # Create path from config file
    #PATH = HOME + cfg.PATH[1:]
    if PATH.startswith("~"):
        PATH = cfg.HOME + PATH[1:]

    if not os.path.exists(PATH):
        os.makedirs(PATH)
        print("Creating", NAME, "directory for datapoint table:", PATH)
    else:
        print(NAME, "directory already exists!")

def main():
    # Create database path
    DB_EXISTS = os.path.exists(DB_PATH)

    if DB_EXISTS == True:
        print("Database exists in file:", cfg.database_file, "\nNew database won't be created!")
    else:
        print("Creating Database!")

    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()

    # Create sources_collection
    try:
        c.execute("""CREATE TABLE sources_collection(
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
                organization text,
                abstract text,
                path_to_bibfile text,
                date text,
                tag_1 text,
                tag_2 text,
                tag_3 text,
                tag_4 text,
                tag_5 text
            )""")

    except sqlite3.OperationalError:
        print("Table already exists: sources_collection")


    # Create datapoint_collection
    try:
        c.execute("""CREATE TABLE datapoint_collection(
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
            )""")

    except sqlite3.OperationalError:
        print("Table already exists: datapoint_collection")

    # Create citation_collection
    try:
        c.execute("""CREATE TABLE citation_collection(
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
            )""")

    except sqlite3.OperationalError:
        print("Table already exists: datapoint_collection")

    create_content_directory(cfg.Str_path_content_directory, "content")
    create_content_directory(cfg.Str_path_citation_directory, "citation")


if __name__ == "__main__":
    main()
