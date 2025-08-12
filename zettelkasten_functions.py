#!/usr/bin/python

import os
import sqlite3
import argparse
import shutil
import re
import textwrap
import main_config as cfg

# This file provides functions which are used on a regular base for the zettelkasten.

def convert_to_org_source(input_dic_list):
    # Converts a source dictionary-list to org codeblock formatted string
    # Origin: dictionary comes e.g. pulled from a .bib-file or the database

    codeblock = ""

    for e in input_dic_list:
        codeblock += org_format_source(e)
        codeblock += "\n"

    return codeblock

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

        CITEKEY = rest[0].strip("\n")

        # Create base for dictonary
        return_dic = {"type": ENTRYTYPE, "citekey": CITEKEY, "path_to_bibfile": BIB_FILE}

        del rest[0]
        # print(rest[-1])
        rest[-1] = rest[-1].split("\n")[0]
        #print(rest[-1])
        #del rest[-1]

        # Strip elements of entry data
        for attribute_line in rest:
            attribute_type = attribute_line.split("=")[0]
            if attribute_type != "}":
                attribute_type = attribute_type.strip()
                attribute_value = attribute_line.split("=", 1)[1]
                attribute_value = attribute_value.strip()
                attribute_value = attribute_value.strip("\"")
                attribute_value = attribute_value.strip("{}")

                return_dic[attribute_type] = attribute_value

        return_list.append(return_dic)

    return return_list

def convert_to_biblatex(input_dic):
    # Converts a dictionary to a biblatex entry.

    blacklist_keys = ["type","citekey","file","id"]

    OUTPUT_STRING = "@"
    OUTPUT_STRING += input_dic["type"]
    OUTPUT_STRING += "{" + input_dic["citekey"] + ",\n"

    for key, value in input_dic.items():
        if key not in blacklist_keys and value != "":
            OUTPUT_STRING += "\t" + key + "\t\t= {" + str(value) + "},\n"


    OUTPUT_STRING = OUTPUT_STRING[:-2] + "\n}"

    return OUTPUT_STRING


def extract_quote_blocks_from_file(path, bool_type):
    with open(path, encoding='utf-8') as f:
        content = f.read()

    if bool_type == "quote":
        REGEX = r'^\#\+BEGIN_SRC\s+quote\s*(.*?)\n(.*?)^\#\+END_SRC'
    elif bool_type == "source":
        REGEX = r'^\#\+BEGIN_SRC\s+source\s*(.*?)\n(.*?)^\#\+END_SRC'
    else:
        REGEX = r'^\#\+BEGIN_SRC\s+datapoint\s*(.*?)\n(.*?)^\#\+END_SRC'

    pattern = re.compile(REGEX, re.MULTILINE | re.DOTALL)

    # pattern = re.compile(r'^\#\+BEGIN_SRC\s+quote\s*(.*?)\n(.*?)^\#\+END_SRC', re.MULTILINE | re.DOTALL)

    results = []
    for match in pattern.findall(content):
        raw_params, body = match
        # params = dict(re.findall(r':(\w+)\s+"?([^"\s]+)"?', raw_params))

        params = re.findall(r':(\w+)\s+(?:"([^"]+)"|(\S+))', raw_params)

        attributes = {key: val1 if val1 else val2 for key, val1, val2 in params}

        results.append({
            'file': str(path),
            'params': attributes,
            'content': body.strip()
        })

    return results


def correct_home_path(INPUT_PATH):
    # This function takes the INPUT_PATH, changes the "~" to the users home directory and checks if the file exisits.
    # Todo: Check if input is viable as a path
    if INPUT_PATH.startswith("~"):
        OUTPUT_PATH = cfg.HOME + INPUT_PATH[1:]
    else:
        OUTPUT_PATH  = INPUT_PATH

    return OUTPUT_PATH

def check_file_exists(PATH):
    if os.path.isfile(PATH):
        return True
    else:
        return False

def get_column_names(TABLENAME, database = correct_home_path(cfg.database_file)):
    # Creates a list of column names of a table
    conn = sqlite3.connect(database)
    c = conn.cursor()
    sql_command = "SELECT * FROM " + TABLENAME + ";"
    cursor = c.execute(sql_command)

    # Create column list
    COLUMN_LIST = list(map(lambda x: x[0], cursor.description))
    c.close()

    return COLUMN_LIST


def drop_table(TABLENAME, DATBASE):
    conn = sqlite3.connect(DATBASE)

    try:
        c = conn.cursor()

        command = "DROP TABLE " + TABLENAME + ";"

        c.execute(command)
    except:
        print("operational Erororor!")

    finally:
        conn.commit()

    return

def key_conversion(key, table):
    # This function is supposed to modify the input key depending on the table.

    if key == "citekey" and table != 1:
        key = "s.citekey"

    if key == "note" and table != 1:
        key = "p.note"
    # else:
    #     key = "s.note"

    if key == "path" and table == 1:
        key = "path_to_bibfile"

    return key

def get_tag_list():
    # Makes a query to the database and compiles a tuple of all tags used.
    tag_list = []
    return_list = db_select_query(1, {}, query_all_bool = True, database = correct_home_path(cfg.database_file))

    for i in return_list:
        if i["tags"] != "":
            tmp_list = i["tags"].split(",")
            for e in tmp_list:
                tag_list.append(e.strip().lower())

    tag_list = set(tag_list)

    return tag_list


def db_select_query(table, query_dict, query_all_bool = False, database = correct_home_path(cfg.database_file)):
    # Make a query to the database.
    # Constructs all the WHERE conditions from key: value pairs of the input dictionary.
    # Returns a dictionary with all (joined) values
    # s.<key> = key from sources
    # p.<key> = key from datapoints / quotes

    # This is the standard sql select command
    return_list = []
    where_list = []

    table = int(table)

    # print(query_all_bool)

    if query_all_bool == False:
        if table == 1:
            # print("Choosing only sources")
            sql_command = "SELECT * FROM  sources_collection WHERE"
        else:
            sql_command = "SELECT * FROM points_collection p INNER JOIN sources_collection s ON p.citekey = s.citekey WHERE"
            if table == 2:
                # print("Choosing only datapoints")
                where_list.append("p.type LIKE 'datapoint' AND")
            elif table == 3:
                # print("Choosing only quotes")
                where_list.append("p.type LIKE 'quote' AND")


        # Construct WHERE conditions from input dictionary
        for key, value in query_dict.items():
            key = key_conversion(key, table)

            # print(key)
            # print(value)

            where_list.append(key + " LIKE '%" + value + "%' AND")

        # Construct SQL where conditions
        for i in where_list:
            sql_command += " " + i + " "

        sql_command = sql_command[:-5] + ";"


    else:
        if table == 1:
            # print("Choosing only sources")
            sql_command = "SELECT * FROM  sources_collection "
        else:
            sql_command = "SELECT * FROM points_collection p INNER JOIN sources_collection s ON p.citekey = s.citekey "
            if table == 2:
                # print("Choosing only datapoints")
                sql_command += "WHERE p.type LIKE 'datapoint'"
            elif table == 3:
                # print("Choosing only quotes")
                sql_command += "WHERE p.type LIKE 'quote'"

        sql_command += ";"



    # Debugging
    # print(sql_command)

    try:
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(sql_command)
        result = c.fetchall()

        for row in result:
            return_list.append(dict(row))

        conn.commit()

    except Exception as e:
        print(e)

    # finally:
    #     conn.commit()


    return return_list

# def db_insert_point(input_command, point_type, citekey, page, file, note, content, database = correct_home_path(cfg.database_file)):
def db_insert_point(input_command, value_tuple, database = correct_home_path(cfg.database_file)):
    # Inserts a datapoint or quote into the table

    # Rewrite this command so that the sql command is constructed from a list (type) of values and a string

    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()
        # c.execute(input_command)
        # c.execute(input_command, (point_type, citekey, page, file, note, content))
        c.execute(input_command, value_tuple)

        conn.commit()

    except Exception as e:
        print(value_tuple)
        print(e)

    # finally:
    #     conn.commit()

    return

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

def delete_row(ID, TABLENAME, database = correct_home_path(cfg.database_file)):
    # Deletes the row with the given id
    EXECUTE_COMMAND = "DELETE  FROM " + TABLENAME + " WHERE id = " + str(ID) + ";"

    # Missing error message for table?

    GETPATH_COMMAND = "SELECT path FROM " + TABLENAME + " WHERE id = " + str(ID) + ";"

    try:
        conn = sqlite3.connect(database)
        c = conn.cursor()

        if TABLENAME == cfg.database_datapoints_tablename:
            Str_content_path = cfg.Str_path_datapoint_directory
        elif TABLENAME  == cfg.database_citations_tablename:
            Str_content_path = cfg.Str_path_citation_directory
        else:
            print("Error! The table you chose does not exist!")

        Str_content_path = correct_home_path(Str_content_path)

        for row in c.execute(GETPATH_COMMAND):
             Str_content_path += row[0]

        # Remove content file if it exists
        if os.path.isfile(Str_content_path):
            os.remove(Str_content_path)

        # Delete Row in database
        c.execute(EXECUTE_COMMAND)

        conn.commit()

    except sqlite3.OperationalError as e:
        print("SQL OperationalError. You probably chose a wrong column!")
        print(e)

    return

def pretty_format_datapoint(INPUT_ROW):
    # Formats the output as a pretty datapoint with the path
    OUTPUT_STRING = "ID: " + str(INPUT_ROW[0]) + ": " + INPUT_ROW[1]                    # Add id and citekey
    OUTPUT_STRING += " | Seiten / Stelle: " + INPUT_ROW[2]                              # Add page / location
    OUTPUT_STRING += "\n" + INPUT_ROW[3]                                                # Add Summary
    OUTPUT_STRING += "\n" + "Pfad: " + cfg.Str_path_datapoint_directory + INPUT_ROW[4]  # Add Path

    # Add tags
    OUTPUT_STRING += "\nTags: "
    for i in range(5, 10):
        if INPUT_ROW[i] != "":
            OUTPUT_STRING += INPUT_ROW[i] + ", "

    OUTPUT_STRING = OUTPUT_STRING[:-2]

    return OUTPUT_STRING

def pretty_format_source(input_dic):
    # Formats the output as a pretty source with infos from sources
    # CITATION = input_dic["content"]


    AUTHOR = input_dic["author"]
    TITLE = input_dic["title"]
    YEAR = input_dic["year"]
    ORIGDATE = input_dic["origdate"]
    PUBLISHER = input_dic["publisher"]


    # if CITATION[-1] == "\n":
    #     CITATION = CITATION[:-1]

    OUTPUT_STRING = " - " + AUTHOR                               # Add author
    OUTPUT_STRING += ", " + TITLE                                       # Add title
    OUTPUT_STRING += " ("

    # Only add Origdate if it exists
    if ORIGDATE != "":
        OUTPUT_STRING += ORIGDATE + ", "

    OUTPUT_STRING += YEAR

    if PUBLISHER == None:
        OUTPUT_STRING += ")"
    else:
        OUTPUT_STRING += " " + PUBLISHER + ")"                                    # Add publisher

    OUTPUT_STRING += "\nID: " + str(input_dic["id"]) + " citekey: " + input_dic["citekey"]    # Add id and citekey
    # Add note
    if input_dic["note"] != None:
        OUTPUT_STRING += "\nNote: " + str(input_dic["note"])

    OUTPUT_STRING += "\n"

    return OUTPUT_STRING


def org_format_citation(input_dic):
    # This function converts the input dic from a source into an org(-roam) usable codeblock

    # OUTPUT_STRING = "Bitte beenden Sie noch dise Funktion, ich bitte Sie, schneeeeeeeeell!!!!"

    # return OUTPUT_STRING

    # blacklist for properties that are not part of the .bib-source entry
    OUTPUT_STRING = "#+BEGIN_SRC " + input_dic["type"] + " :citekey "
    OUTPUT_STRING += input_dic["citekey"]
    OUTPUT_STRING += " :page "
    OUTPUT_STRING += input_dic["type"]
    OUTPUT_STRING += " :note \""
    if input_dic["note"] != None:
        OUTPUT_STRING += input_dic["note"]
    OUTPUT_STRING += "\"\n"

    OUTPUT_STRING += input_dic["content"]

    OUTPUT_STRING += "\n"

    OUTPUT_STRING += "#+END_SRC\n"

    return OUTPUT_STRING

def org_format_source(input_dic):
    # This function converts the input dic from a source into an org(-roam) usable codeblock

    # blacklist for properties that are not part of the .bib-source entry
    blacklist_props = ["citekey", "type", "path_to_bibfile", "id"]

    OUTPUT_STRING = "#+BEGIN_SRC source :citekey "
    OUTPUT_STRING += input_dic["citekey"]
    OUTPUT_STRING += " :type "
    OUTPUT_STRING += input_dic["type"]
    # OUTPUT_STRING += input_dic["entrytype"]


    # Add display column?!
    # OUTPUT_STRING += " :display \""

    # if input_dic["display"] != None:
    #     OUTPUT_STRING += input_dic["display"]

    # OUTPUT_STRING += "\"\n"
    OUTPUT_STRING += "\n"

    # Add rest of the key / value pairs
    for key, value in input_dic.items():
        if key not in blacklist_props and value != "":
            # OUTPUT_STRING += key + "\t\t= {" + value + "}\n"
            OUTPUT_STRING += key + " = " + value + "\n"

    OUTPUT_STRING += "#+END_SRC\n"

    return OUTPUT_STRING

def pretty_format_citation(input_dic):
    # Formats the output as a pretty citation / datapoint with infos from sources
    CITATION = input_dic["content"]


    AUTHOR = input_dic["author"]
    TITLE = input_dic["title"]
    YEAR = input_dic["year"]
    ORIGDATE = input_dic["origdate"]
    PUBLISHER = input_dic["publisher"]

    if PUBLISHER == None:
        PUBLISHER = ""

    if CITATION[-1] == "\n":
        CITATION = CITATION[:-1]

    if input_dic["type"] == "quote":
        CITATION = "\"" + CITATION + "\""

    CITATION = textwrap.fill(CITATION, width=60, initial_indent='\t', subsequent_indent='\t')

    # print(textwrap.fill(i, width=100, replace_whitespace=True, drop_whitespace=True, break_on_hyphens=False))

    OUTPUT_STRING = "ID: " + str(input_dic["id"]) + " citekey:  " + input_dic["citekey"]    # Add id and citekey
    # Add note


    if input_dic["note"] != None:
        # NOTE_TEXT += "\nNote:\t\t " + str(input_dic["note"])
        NOTE_TEXT = textwrap.fill(str(input_dic["note"]), width=55, initial_indent='Note:\t\t ', subsequent_indent='     \t\t ')
    else:
        NOTE_TEXT = "\nNote:\t\t -"
        # NOTE_TEXT = textwrap.fill(str(input_dic["note"], width=60, initial_indent='Note:\t\t ', subsequent_indent='     \t\t ')


    OUTPUT_STRING += "\n" + NOTE_TEXT




    OUTPUT_STRING += "\nSeiten / Stelle: " + input_dic["page"]         # Add pages / location
    OUTPUT_STRING += "\n" + CITATION + "\n"                         # Add citation itself

    if AUTHOR == "":
        ADDENDUM =  input_dic["editor"]                               # Add author
    else:
        ADDENDUM =  AUTHOR                               # Add author
    ADDENDUM += ", " + TITLE                                       # Add title
    ADDENDUM += " ("

    # Only add Origdate if it exists
    if ORIGDATE != "":
        ADDENDUM += ORIGDATE + ", "

    ADDENDUM += YEAR + " "                                  # Add publishing year
    ADDENDUM += PUBLISHER + ")"                                    # Add publisher

    ADDENDUM = textwrap.fill(ADDENDUM, width=60, initial_indent='\t- ', subsequent_indent='\t  ')

    OUTPUT_STRING += ADDENDUM + "\n"


    # OUTPUT_STRING = OUTPUT_STRING[:-2]

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
