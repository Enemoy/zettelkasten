#!/usr/bin/python

import sqlite3
import string
import random
import pyperclip
import os
import argparse
import main_config as cfg

# This script checks if the citekeys in datapoints and in citations are still in sources.
def check_citekeys(PATH_TO_DATABASE = cfg.database_file, SOURCES_TABLE = cfg.database_bib_sources_tablename, DATAPOINT_TABLE = cfg.database_datapoints_tablename, CITATIONS_TABLE = cfg.database_citations_tablename):
    # Check if citekeys are still there. Default to the database values in the config file.
    if PATH_TO_DATABASE.startswith("~"):
        PATH_TO_DATABASE = cfg.HOME + PATH_TO_DATABASE[1:]

    # The list of sources citekeys
    list_checkup_reference = []

    # The list of citekeys in datapoints and citations
    list_checkup = []

    # list of signifiers to be returned
    list_return = []

    # Extract all citekeys from sources
    EXECUTE_COMMAND = "SELECT citekey FROM " + SOURCES_TABLE + ";"

    conn = sqlite3.connect(PATH_TO_DATABASE)

    c = conn.cursor()

    for row in c.execute(EXECUTE_COMMAND):
        list_checkup_reference.append(row[0])

    # Extract all citekeys from datapoints
    EXECUTE_COMMAND = "SELECT citekey FROM " + DATAPOINT_TABLE + ";"

    for row in c.execute(EXECUTE_COMMAND):
        if row[0] not in list_checkup:
            list_checkup.append(row[0])

    # Extract all citekeys from citations
    EXECUTE_COMMAND = "SELECT citekey FROM " + CITATIONS_TABLE + ";"

    for row in c.execute(EXECUTE_COMMAND):
        if row[0] not in list_checkup:
            list_checkup.append(row[0])

    # Add all citekeys from list_checkup that are not in list_checkup_reference to the output list.
    for e in list_checkup:
        if e not in list_checkup_reference:
            list_return.append(e)

    return list_return

def main():
    list_output = check_citekeys()

    for e in list_output:
        print(e)


if __name__ == "__main__":
    main()
