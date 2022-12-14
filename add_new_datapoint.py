#!/usr/bin/python

import sqlite3
import string
import random
import pyperclip
import os
import argparse
import main_config as cfg
import zettelkasten_functions as zfn


# This python script will add a new information entry from a preformatted file with information.

Str_manual_description="This script will add a new set of information to the information table in the database."
Str_manual_usage="add_new_datapoint.py [args]"
Str_manual_flag_file="Choose this option if the content of the information is stored in a textfile."
Str_manual_flag_clipboard="Use this option if the content part of the information is stored in the clipboard."
Str_manual_flag_preexisting="This option is used when the whole information set is already stored in a preexisting, properly formatted file."
Str_manual_flag_dryrun="Will only print the SQL-command that will be constructed, without running it on the database."
Str_path_databasefile=cfg.database_file


def create_new_contentfile(FILE_PATH, STORAGE_DIRECTORY, CONTENT_PREX, BOOL_DRYRUN):
    # Creates a new content-file in the corresponding folder an returns the path to the file as a string.
    """
    Todo:
        - check if random filename already exists
    """
    Str_filename_random = ""

    for i in range(30):
        Str_filename_random += random.choice(string.ascii_uppercase)

    Str_path_new_content_file = STORAGE_DIRECTORY + Str_filename_random + ".md"


    if Str_path_new_content_file.startswith("~"):
        Str_path_new_content_file = cfg.HOME + Str_path_new_content_file[1:]

    f = open(Str_path_new_content_file, "w")

    if CONTENT_PREX != None:
        FILE_PATH = CONTENT_PREX

    if BOOL_DRYRUN != True:
        f.write(open(FILE_PATH, "r").read())
    else:
        print(open(FILE_PATH, "r").read())

    f.close()

    # print(Str_path_new_content_file)
    # print(Str_path_new_content_file.split("/")[-1])

    # quit()

    return Str_path_new_content_file.split("/")[-1]


def extract_information(FILE_PATH, CONTENT_PREX, BOOL_DRYRUN):
    # This function will extract the information from the preformatted datafile given as a path

    f = open(FILE_PATH, "r").read()

    lines = f.split("\n")

    # Delete trailing empty line
    del lines[-1]

    Str_dataset_citekey = ""
    Str_dataset_page = ""
    Str_dataset_summary = ""
    List_dataset_tags = []
    Str_dataset_content_path = ""
    Str_dataset_quote_path = ""

    # Extract different information types and assign them to variables
    for line in lines:
        if line.startswith("CITEKEY="):
            Str_dataset_citekey = line.split("=", 1)[1]

        elif line.startswith("PAGE="):
            Str_dataset_page = line.split("=", 1)[1]

        elif line.startswith("SUMMARY="):
            Str_dataset_summary = line.split("=",1 )[1]

        elif line.startswith("TAGS="):
            List_dataset_tags = line.split("=", 1)[1].split(",",4)

        elif line.startswith("CONTENT="):
            Str_entry_type = "CONTENT"
            Str_dataset_content_path = line.split("=", 1)[1]

        elif line.startswith("QUOTE="):
            Str_entry_type = "QUOTE"
            Str_dataset_quote_path = line.split("=", 1)[1]


    # Extract Tags from taglist
    try:
        Str_dataset_tag_1 = List_dataset_tags[0]
    except IndexError:
        Str_dataset_tag_1 = ""

    try:
        Str_dataset_tag_2 = List_dataset_tags[1]
    except IndexError:
        Str_dataset_tag_2 = ""

    try:
        Str_dataset_tag_3 = List_dataset_tags[2]
    except IndexError:
        Str_dataset_tag_3 = ""

    try:
        Str_dataset_tag_4 = List_dataset_tags[3]
    except IndexError:
        Str_dataset_tag_4 = ""

    try:
        Str_dataset_tag_5 = List_dataset_tags[4]
    except IndexError:
        Str_dataset_tag_5 = ""

    if Str_dataset_citekey == "":
         print("No citekey given! Aborting the process!")
         quit()

    if Str_dataset_page == "":
         print("No page given! Aborting the process!")
         quit()

    if Str_dataset_summary == "" and Str_entry_type == "CONTENT":
         print("No summary given! Aborting the process!")
         quit()

    if Str_dataset_tag_1 == "":
         print("No tags given! Hopefully you did this on purpose!")
         quit()


    Str_quote_committed = ""
    Str_content_committed = ""

    # Erstellt Datei mit Inhalt in richtigem Ordner
    if Str_entry_type == "CONTENT":
        Str_content_committed = create_new_contentfile(Str_dataset_content_path, cfg.Str_path_datapoint_directory, CONTENT_PREX, BOOL_DRYRUN)

    elif Str_entry_type == "QUOTE":
        Str_quote_committed = create_new_contentfile(Str_dataset_quote_path, cfg.Str_path_citation_directory , CONTENT_PREX, BOOL_DRYRUN)

    else:
        print("No path given to a temporary content file. You fucked up!")
        quit()

    # Replace relevant characters
    Str_dataset_summary = Str_dataset_summary.replace("'", "’")
    Str_dataset_summary = Str_dataset_summary.replace("\"", "\\\"")


    content_path = Str_content_committed
    quote_path = Str_quote_committed

    # Construct SQL-Command for either citation or datapoint collection.
    if Str_content_committed != "" and Str_quote_committed == "":
        sql_values = "'" + Str_dataset_citekey + "','"
        sql_values += Str_dataset_page + "','"
        sql_values += Str_dataset_summary + "','"
        sql_values += content_path + "','"
        sql_values += Str_dataset_tag_1 + "','"
        sql_values += Str_dataset_tag_2 + "','"
        sql_values += Str_dataset_tag_3 + "','"
        sql_values += Str_dataset_tag_4 + "','"
        sql_values += Str_dataset_tag_5 + "'"

        sql_command = "INSERT INTO " + cfg.database_datapoints_tablename
        sql_command += "(citekey,page,summary,path,tag_1,tag_2,tag_3,tag_4,tag_5) VALUES(" + sql_values + ")"

    elif Str_content_committed == "" and Str_quote_committed != "":
        # sql_values = "'" + Str_dataset_citekey + "','" + Str_dataset_page + "','" + quote_path + "','" + Str_dataset_tag_1 + "','" + Str_dataset_tag_2 + "','" + Str_dataset_tag_3 + "','" + Str_dataset_tag_4 + "','" + Str_dataset_tag_5 + "'"
        # sql_command = "INSERT INTO " + cfg.database_citations_tablename  + "(citekey,page,path,tag_1,tag_2,tag_3,tag_4,tag_5) VALUES(" + sql_values + ")"
        sql_values = "'" + Str_dataset_citekey + "','"
        sql_values += Str_dataset_page + "','"
        sql_values += quote_path + "','"
        sql_values += Str_dataset_tag_1 + "','"
        sql_values += Str_dataset_tag_2 + "','"
        sql_values += Str_dataset_tag_3 + "','"
        sql_values += Str_dataset_tag_4 + "','"
        sql_values += Str_dataset_tag_5 + "'"

        sql_command = "INSERT INTO " + cfg.database_citations_tablename
        sql_command += "(citekey,page,path,tag_1,tag_2,tag_3,tag_4,tag_5) VALUES(" + sql_values + ")"

    return sql_command

def main():
    # Set up the argument input
    parser = argparse.ArgumentParser(description=Str_manual_description, usage=Str_manual_usage, add_help=True)
    parser.add_argument("-f", "--file", type=str, help=Str_manual_flag_file)
    parser.add_argument("-c", "--clipboard", action="store_true", help=Str_manual_flag_clipboard)
    #parser.add_argument("-t", "--terminal", action="store_true", help=Str_manual_flag_terminal)
    parser.add_argument("-p", "--preexisting", type=str, help=Str_manual_flag_preexisting)
    parser.add_argument("-d", "--dryrun", action="store_true", help=Str_manual_flag_dryrun)
    args = parser.parse_args()

    # Take content from the system-clipboard and put it into a temporary file
    if args.clipboard:
        Input_content = pyperclip.paste()
        Int_random_01 = random.randint(100000, 1000000)

        Str_path_clipboard_content = "/tmp/clipboard_" + str(Int_random_01)

        t = open(Str_path_clipboard_content, "w")
        t.write(Input_content)
        t.close()

    else:
        Str_path_clipboard_content = None


    # This is necesarry for some reason, I can't figure out why
    Str_path_database = Str_path_databasefile

    if Str_path_database.startswith("~"):
        Str_path_database = cfg.HOME + Str_path_database[1:]

    if args.preexisting:
        Str_path_preexisting = args.preexisting
        Str_command_sql_addcontent = extract_information(Str_path_preexisting, Str_path_clipboard_content, args.dryrun)
    else:
        print("Error!")

    # Only print SQL-command with the dryrun flag, without executing it
    if args.dryrun:
        print(Str_command_sql_addcontent)
    else:
        zfn.execute_sql_command(Str_command_sql_addcontent, Str_path_database)


if __name__ == "__main__":
    main()
