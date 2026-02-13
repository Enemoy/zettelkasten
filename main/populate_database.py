#!/usr/bin/python

import sqlite3
import string
import random
import pyperclip
import os
import time
import argparse
import sys

sys.path.insert(0, '/home/simon/.bin/zettelkasten/')
import create_database as cbd
import main_config as cfg
import zettelkasten_functions as zfn


# Schlachtplan:
# 1. Extractor aufrufen
# 2. Formatierung zu SQL-Befehlen
# 3. Datenbankstruktur neu aufsetzen → nur eine Tabelle!
# 4. SQL-Befehle ausführen

Str_manual_description="This script will scan the org files and add all quotes and datapoints to the corresponding tables."
Str_manual_usage="add_new_datapoint.py [args]"
Str_manual_flag_file="Choose this option if the content of the information is stored in a textfile."
Str_manual_flag_quiet="Don't print warnings and counts."
Str_manual_flag_clipboard="Use this option if the content part of the information is stored in the clipboard."
Str_manual_flag_preexisting="This option is used when the whole information set is already stored in a preexisting, properly formatted file."
Str_manual_flag_dryrun="Will only print the SQL-command that will be constructed, without running it on the database."
Str_manual_flag_update="If set, database will not be updated but fully repopulated. [Under construction]"
Str_path_databasefile=cfg.database_file

def org_citation_extractor(org_filelist, entry_type):

    warning_list = []
    return_list = []

    for file in org_filelist:

        path_to_org = cfg.HOME + cfg.Org_roam_dir[1:] + file

        if not file.endswith(".org"):
            continue

        tmp_list, tmp_warnings = zfn.extract_quote_blocks_from_file(path_to_org, entry_type)

        for i in tmp_list:

            if entry_type == "source":
                return_list.append(format_source(i, entry_type))
            else:
                return_list.append(format_citation(i, entry_type))

        for i in tmp_warnings:
            warning_list.append(i)


    return return_list, warning_list

def format_source(i, entry_type):

    tmp_dict = {}

    tmp_dict["file"] = i["file"]
    tmp_dict["citekey"] = i["params"]["citekey"]
    tmp_dict["type"] = i["params"]["type"]
    tmp_dict["sid"] = i["params"]["sid"]
    tmp_dict["display"] = i["params"]["display"]

    for line in i["content"].strip().split('\n'):
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            tmp_dict[key] = value

    return tmp_dict


def format_citation(i, entry_type):
    tmp_dict = {}

    try:
        tmp_dict["content"] = i["content"]
        tmp_dict["file"] = i["file"]
        tmp_dict["citekey"] = i["params"]["citekey"]
        tmp_dict["page"] = i["params"]["page"]
        tmp_dict["cid"] = i["params"]["cid"]
        tmp_dict["display"] = i["params"]["display"]
        tmp_dict["type"] = entry_type

    except KeyError as e:
        print("There was a parameter missing, skipping entry!")

    try:
        tmp_dict["info"] = i["params"]["info"]
    except KeyError as e:
        debug = 0
        if debug == 1:
            print(e)

    return tmp_dict

def sql_constructor(input_dic):
    tablename = cfg.database_bib_sources_tablename
    sid_or_cid = "sid"

    if input_dic["type"] == "quote" or input_dic["type"] == "datapoint":
        tablename = cfg.points_tablename
        sid_or_cid = "cid"

    sql_command_types = "INSERT INTO " + tablename + "("
    sql_command_values = "VALUES("
    update_command = " ON CONFLICT(" + sid_or_cid + ") DO UPDATE SET "
    # addendum_command =

    value_tuple = ()
    update_tuple = ()

    for key, value in input_dic.items():
        sql_command_types += key + ","
        sql_command_values += "?,"
        value_tuple = value_tuple + (value,)

        if key != sid_or_cid:
            update_command += key + "=?, "
            update_tuple = update_tuple + (value,)

    sql_command = sql_command_types[:-1] + ") " + sql_command_values[:-1] + ") " + update_command[:-2] + ";"

    value_tuple = value_tuple + update_tuple

    # print(value_tuple)
    # print(sql_command)

    zfn.db_insert_point(sql_command, value_tuple)

    return input_dic


def main():
    parser = argparse.ArgumentParser(description=Str_manual_description, usage=Str_manual_usage, add_help=True)
    parser.add_argument("-f", "--file", type=str, help=Str_manual_flag_file)
    parser.add_argument("-c", "--clipboard", action="store_true", help=Str_manual_flag_clipboard)
    parser.add_argument("-p", "--preexisting", type=str, help=Str_manual_flag_preexisting)
    parser.add_argument("-d", "--dryrun", action="store_true", help=Str_manual_flag_dryrun)
    parser.add_argument("-q", "--quiet", action="store_false", help=Str_manual_flag_quiet)
    parser.add_argument("-u", "--update", action="store_false", help=Str_manual_flag_update)
    args = parser.parse_args()

    if not args.update:
        # First, empty out database
        print("Repopulating, not updating!")
        zfn.drop_table(zfn.correct_home_path(cfg.points_tablename), zfn.correct_home_path(cfg.database_file))
        zfn.drop_table(zfn.correct_home_path(cfg.database_bib_sources_tablename), zfn.correct_home_path(cfg.database_file))
        cbd.create_datapoints_table(zfn.correct_home_path(cfg.database_file), zfn.correct_home_path(cfg.points_tablename))
        cbd.create_sources_table(zfn.correct_home_path(cfg.database_file), zfn.correct_home_path(cfg.database_bib_sources_tablename))
    else:
        print("Updating, not repopulating!")

    org_roam_path = cfg.HOME + cfg.Org_roam_dir[1:]

    f = [cfg.Org_roam_quotes, cfg.Org_roam_datapoints]

    for (dirpath, dirnames, filenames) in os.walk(org_roam_path):
        f.extend(filenames)
        break

    f = list(set(f))

    entry_list = []
    warning_list = []

    types = ["quote", "datapoint", "source" ]

    for t in types:
        tmp_entries, tmp_warnings = org_citation_extractor(f, t)
        entry_list.extend(tmp_entries)
        warning_list.extend(tmp_warnings)

    sql_list = []

    counter = 0

    for i in entry_list:
        if i != 0:
            sql_list.append(sql_constructor(i))
            counter += 1


    cid_list = zfn.extract_list_cid()
    highest_cid = cid_list.pop(-1)
    cid_list.pop(0)

    sid_list = zfn.extract_list_cid(table=cfg.database_bib_sources_tablename)
    highest_sid = sid_list.pop(-1)
    sid_list.pop(0)

    if args.quiet:
        for w in warning_list:
            print(w)

        output_string = "Highest cid: " + str(highest_cid) + "\nFree cids are: "

        for i in cid_list:
            output_string += str(i) + ", "

        output_string = output_string.strip(', ') + "\nHighest sid: " + str(highest_sid) + "\nFree sids are: "

        for i in sid_list:
            output_string += str(i) + ", "

        print(output_string.strip(', '))





if __name__ == "__main__":
    main()

