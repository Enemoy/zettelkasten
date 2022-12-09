#!/usr/bin/python

import os
import sqlite3
import argparse
import shutil
import main_config as cfg

#This file provides functions which are used on a regular base for the zettelkasten.

def correct_home_path(INPUT_PATH):
    # This function takes the INPUT_PATH, changes the "~" to the users home directory and checks if the file exisits.
    # Todo: Check if input is viable as a path
    if INPUT_PATH.startswith("~"):
        OUTPUT_PATH = cfg.HOME + INPUT_PATH[1:]
    else:
        OUTPUT_PATH  = INPUT_PATH

    return OUTPUT_PATH


def execute_sql_command(input_command, database = correct_home_path(cfg.database_file)):
    # executes the sql-command onto the database

    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute(input_command)
        conn.commit()

    except sqlite3.OperationalError as e:
        print("SQL OperationalError. You probably chose a wrong column!")
        print(e)
        # print("Input command: ")
        # print(input_command)

    return

def pretty_format_source(INPUT_ROW):
    # Formats the outout as a pretty source (maybe even in APA)?
    OUTPUT_STRING = "ID: " + str(INPUT_ROW[0]) + ": " + INPUT_ROW[1]

    return OUTPUT_STRING

def pretty_format_datapoint(INPUT_ROW):
    # Formats the output as a pretty datapoint with the path
    OUTPUT_STRING = "ID: " + str(INPUT_ROW[0]) + ": " + INPUT_ROW[1]    # Add id and citekey
    OUTPUT_STRING += " | Seiten / Stelle: " + INPUT_ROW[2]              # Add page / location
    OUTPUT_STRING += "\n" + INPUT_ROW[3]                                # Add Summary
    OUTPUT_STRING += "\n" + "Pfad: " + INPUT_ROW[4]                     # Add Path

    # Add tags
    OUTPUT_STRING += "\nTags: "
    for i in range(5, 9):
        if INPUT_ROW[i] != "":
            OUTPUT_STRING += INPUT_ROW[i] + ", "

    OUTPUT_STRING = OUTPUT_STRING[:-2]

    return OUTPUT_STRING

def pretty_format_citation(INPUT_ROW):
    # Formats the output as a pretty citation with infos from sources
    #Get quote from file
    f = open(INPUT_ROW[3], "r")
    CITATION = f.read()
    f.close()

    # Gather source row
    conn = sqlite3.connect(correct_home_path(cfg.database_file))
    c = conn.cursor()
    conn.commit()

    EXECUTE_COMMAND = "SELECT * FROM " + cfg.database_bib_sources_tablename + " WHERE citekey LIKE '" + INPUT_ROW[1] + "';"

    try:
        for row in c.execute(EXECUTE_COMMAND):
            AUTHOR = row[3]
            TITLE = row[4]
            YEAR = row[5]

    except Exception as e:
        print(e)

    if CITATION[-1] == "\n":
        CITATION = CITATION[:-1]

    OUTPUT_STRING = "ID: " + str(INPUT_ROW[0]) + ": " + INPUT_ROW[1]    # Add id and citekey
    OUTPUT_STRING += " | Seiten / Stelle: " + INPUT_ROW[2]              # Add pages / location
    OUTPUT_STRING += "\n\t\"" + CITATION + "\""                         # Add citation itself
    OUTPUT_STRING += "\n\t\t - " + AUTHOR                               # Add author
    OUTPUT_STRING += ", " + TITLE                                       # Add title
    OUTPUT_STRING += " (" + YEAR + " p.d.)"                             # Add publishing year

    # Add tags
    OUTPUT_STRING += "\nTags: "
    for i in range(5, 9):
        if INPUT_ROW[i] != "":
            OUTPUT_STRING += INPUT_ROW[i] + ", "

    OUTPUT_STRING = OUTPUT_STRING[:-2]

    return OUTPUT_STRING

def pretty_print(INPUT_ID, TABLENAME, database = correct_home_path(cfg.database_file)):
    # This functions prints an entry in a database in a pretty way instead of just printing the column value
    conn = sqlite3.connect(database)
    c = conn.cursor()
    conn.commit()

    EXECUTE_COMMAND = "SELECT * FROM " + TABLENAME + " WHERE id = " + str(INPUT_ID) + ";"

    OUTPUT_STRING = ""
    try:
        for row in c.execute(EXECUTE_COMMAND):
            # Format the string depending on the table that it comes from:
            # Format output for source entry
            if TABLENAME == cfg.database_bib_sources_tablename:
                OUTPUT_STRING = pretty_format_source(row)

            # Format output for datapoint
            elif TABLENAME == cfg.database_datapoints_tablename:
                OUTPUT_STRING = pretty_format_datapoint(row)

            # Format output for citation
            elif TABLENAME == cfg.database_citations_tablename :
                OUTPUT_STRING = pretty_format_citation(row)

    except Exception as e:
        print(e)

    return OUTPUT_STRING

def main():
    print("Use the functions from this script instead of calling it directly!")


if __name__ == "__main__":
    main()
