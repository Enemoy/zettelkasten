#!/usr/bin/python

import sqlite3
import bib_file_converter
import os
import argparse
import main_config as cfg
import zettelkasten_functions as zfn

Str_manual_usage="zettelkasten convert [-d DIRECTORY] [-f FILES] [-r]"
Str_manual_description="This script converts contents of .bib-files into entries for a database and adds it to the corresponding table in the corresponding database configured in the config file."
Str_flag_repopulate="Give this flag, if the sources_collection table should be emptied and repopulated."
Str_flag_directory="Adds the entries of all the .bib-files in the directory to the database."
Str_flag_file="Adds the content of a single file to the database."

def repopulate(DATBASE, TABLENAME):
    # Empties the content of the sources_collection table in the database.
    conn = sqlite3.connect(DATBASE)

    c = conn.cursor()

    command = "DELETE FROM " + TABLENAME + ";"

    c.execute(command)

    print("Table emptied!")

    conn.commit()

    c.close()

    return

def convert_bibfile_folder(BIBFILE_FOLDER, Str_path_database_local):
    # Converts all .bib-files into entries in the database
    bib_file_list = []
    for root, dirs, files in os.walk(BIBFILE_FOLDER):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith(".bib"):
                if os.path.getsize(path) != 0:
                    database_fillup(path, Str_path_database_local, cfg.database_bib_sources_tablename)
                else:
                    print("The file", path, "is empty!")

def convert_bibfile_single(BIBFILE_PATH, Str_path_database_local):
    # Converts a single .bib-file into entries in the database.
    if BIBFILE_PATH.startswith("~"):
        BIBFILE_PATH = cfg.HOME + BIBFILE_PATH[1:]
    if BIBFILE_PATH.endswith(".bib"):
        if os.path.getsize(BIBFILE_PATH) != 0:
            database_fillup(BIBFILE_PATH, Str_path_database_local, cfg.database_bib_sources_tablename)
        else:
            print("The file", BIBFILE_PATH, "is empty!")

def check_citekey_double(DATBASE, TABLENAME, INPUT_DIC):
    # Überprüft, ob der Citekey schon in der Tabelle vorhanden ist.
    conn = sqlite3.connect(DATBASE)
    c = conn.cursor()

    COMMAND_TITLES = "SELECT title FROM " + TABLENAME + " WHERE citekey = '" + INPUT_DIC["citekey"] + "';"
    COMMAND_PATHS = "SELECT path_to_bibfile FROM " + TABLENAME + " WHERE citekey = '" + INPUT_DIC["citekey"] + "';"
    NEW_PATH = INPUT_DIC["path_to_bibfile"]
    TITLE_LIST = []
    PATH_LIST = ""
    for row in c.execute(COMMAND_TITLES):
        TITLE_LIST += row

    for row in c.execute(COMMAND_PATHS):
        PATH_LIST = row[0]

    if NEW_PATH in PATH_LIST:
        return "EMPTY"

    if bool(TITLE_LIST):
        ERROR_STRING = "The entry under this citekey is already in the database. The name of the entries are: "
        for e in TITLE_LIST:
            ERROR_STRING += e + "; "

        return PATH_LIST

    return None



def convert_to_sql_command(input_dic, database, tablename, column_names_mixed):
    # Creates an SQL-Insert Command out of the values of the dictonary and adds the content to the database.
    INSERT_COMMAND = "INSERT INTO " + tablename + "("

    column_names = []

    for key in column_names_mixed:
        column_names.append(key.lower())

    keylist = input_dic.keys()

    for key in keylist:
        #Check for double based on citekey
        # if key == "ISSN":
        #     print(input_dic)
        if key == "citekey":
            CITEKEY_DOUBLE_BOOL = check_citekey_double(database, tablename, input_dic)
        if key.lower() in column_names:
            INSERT_COMMAND += key + ", "

    try:
        TEMP_AUTHOR = input_dic["author"]
    except:
        try:
            TEMP_AUTHOR = input_dic["editor"]
        except:
            ERROR_STRING = "No author or editor found for entry: " + input_dic["title"] + " (" + input_dic["bibfile"] + ")"
            print(ERROR_STRING)
            quit()

    INSERT_COMMAND = INSERT_COMMAND[:-2]
    INSERT_COMMAND += ") VALUES("

    for key in keylist:
        if key.lower() in column_names:
            # Replacing certain characters to not producte sql syntax errors
            # This should be fixed later because it's lazy programming
            key_value = input_dic[key]
            key_value = key_value.replace("'", "’")

            INSERT_COMMAND += "'" + key_value + "', "
        else:
            print("Key not in the list:", key, "in", input_dic["path_to_bibfile"])


    INSERT_COMMAND = INSERT_COMMAND[:-2]
    INSERT_COMMAND += ");"

    # Return the insert command string if the citekey is not already in the database
    if CITEKEY_DOUBLE_BOOL == None:
        return INSERT_COMMAND

    # Add the new bibfile path to the filed in the database
    OLD_BIBFILE_VALUE = input_dic["path_to_bibfile"]

    # if is already in the path list of the db entry, then it won't be added (keyword is "EMPTY")
    if CITEKEY_DOUBLE_BOOL == "EMPTY":
        NEW_BIBFILE_VALUE = OLD_BIBFILE_VALUE
    else:
        NEW_BIBFILE_VALUE = OLD_BIBFILE_VALUE + ";" + CITEKEY_DOUBLE_BOOL

    #returns an SQL Command that adds the new path to the entry
    INSERT_COMMAND = "UPDATE " + tablename + " SET path_to_bibfile='" + NEW_BIBFILE_VALUE + "' WHERE citekey='" + input_dic["citekey"] + "'"

    return INSERT_COMMAND

    return None


def create_entry_list(BIB_FILE):
    # returns a list with dictonaries.
    # The dictonaries contain the information about the database entry.

    f = open(BIB_FILE, "r").read()

    content = f.split("@", 1)
    content = content[1]

    entries = content.split("\n@")

    return_list = []

    for entry in entries:
        # Extracts the different parts of the entry-data from the string
        ENTRYTYPE = entry.split("{", 1)[0]
        rest = entry.split("{", 1)[1]

        rest = rest.split(",\n")

        CITEKEY = rest[0]

        # Create base for dictonary
        return_dic = {"entrytype": ENTRYTYPE, "citekey": CITEKEY, "path_to_bibfile": BIB_FILE}

        del rest[0]
        # print(rest[-1])
        rest[-1] = rest[-1].split("\n")[0]
        #print(rest[-1])
        #del rest[-1]

        # Strip elements of entry data
        for e in rest:
            attribute_type = e.split("=")[0]
            if attribute_type != "}":
                attribute_type = attribute_type.strip()
                attribute_value = e.split("=")[1]
                attribute_value = attribute_value.strip()
                attribute_value = attribute_value.strip("\"")
                attribute_value = attribute_value.strip("{}")

                return_dic[attribute_type] = attribute_value

        return_list.append(return_dic)

    return return_list

def database_fillup(BIB_FILE, STR_FILENAME_DATABASE, BIB_TABLENAME):
    # Creating list with column names to exclude data that is not assignable to a column
    List_database_columnnames = zfn.get_column_names(BIB_TABLENAME)

    entry_list = create_entry_list(BIB_FILE)

    for e in entry_list:
        Str_command_sqlexecute_final = convert_to_sql_command(e, STR_FILENAME_DATABASE, BIB_TABLENAME, List_database_columnnames)
        if Str_command_sqlexecute_final != None:
            zfn.execute_sql_command(Str_command_sqlexecute_final, STR_FILENAME_DATABASE)

    return

def main():
    parser = argparse.ArgumentParser(description=Str_manual_description, usage=Str_manual_usage, add_help=True)
    parser.add_argument("-r", "--refresh", action="store_true", help=Str_flag_repopulate)
    parser.add_argument("-d", "--directory", action="append", help=Str_flag_directory)
    parser.add_argument("-f", "--file", action="append", help=Str_flag_file)
    args = parser.parse_args()

    if cfg.database_file.startswith("~"):
        Str_path_database_local = cfg.HOME + cfg.database_file [1:]
    else:
        Str_path_database_local  = cfg.database_file

    if cfg.Str_path_bibfolder.startswith("~"):
        Str_path_bibfolder_local = cfg.HOME + cfg.Str_path_bibfolder[1:]
    else:
        Str_path_bibfolder_local  = cfg.Str_path_bibfolder

    if args.refresh:
        print("Repopulating...")
        repopulate(Str_path_database_local, cfg.database_bib_sources_tablename)
    else:
        print("Not repopulating...")

    # If no input files are given, the default folder of bib-files is chosen.
    if args.directory == None and args.file == None:
        print("Defaulting! Using all .bib-files in the default folder of the config file.")
        convert_bibfile_folder(Str_path_bibfolder_local, Str_path_database_local)

    # Convert every file in the directories given as arguments.
    if args.directory:
        for d in args.directory:
            convert_bibfile_folder(d, Str_path_database_local)

    # Convert every file given as an argument.
    if args.file:
        for f in args.file:
            convert_bibfile_single(f, Str_path_database_local)

if __name__ == "__main__":
    main()
