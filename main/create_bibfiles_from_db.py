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
import main_config as cfg
import zettelkasten_functions as zfn
import create_database as cbd

Str_manual_description="This script will create bib-file for each tag found in the database and add the corresponding entries. Alternatively, it will create a bib file with all sources."
Str_manual_usage="create_bibfile_from_db.py [args]"
Str_manual_main="Will make the program create the general bib file with all the entries. It uses the path from the config."
Str_manual_all="Will make the program create a bibfile for each tag."
# Str_manual_flag_clipboard="Use this option if the content part of the information is stored in the clipboard."
Str_manual_flag_file="Choose a file to put the output into. If empty, will print to configured file. If file is \"-\", it will print to standard out."
Str_manual_flag_tag="The tag in the database, the .bib-file will be created from."
Str_path_databasefile=cfg.database_file

def tagged_entries(tag):
    query_dict = {"tags": tag}

    return_list = []

    whole_list = zfn.db_select_query(1, query_dict, query_all_bool = False, database = zfn.correct_home_path(cfg.database_file))

    for i in whole_list:
        return_list.append(zfn.convert_to_biblatex(i))

    return return_list

def all_entries():
    query_dict = {}

    return_list = []

    whole_list = zfn.db_select_query(1, query_dict, query_all_bool = True, database = zfn.correct_home_path(cfg.database_file))

    for i in whole_list:
        return_list.append(zfn.convert_to_biblatex(i))

    return return_list

def main():
    parser = argparse.ArgumentParser(description=Str_manual_description, usage=Str_manual_usage, add_help=True)
    parser.add_argument("-m", "--main", action="store_true", help=Str_manual_main)
    parser.add_argument("-a", "--all", action="store_true", help=Str_manual_all)
    parser.add_argument("-f", "--file", type=str, help=Str_manual_flag_file)
    parser.add_argument("-t", "--tag", type=str, help=Str_manual_flag_tag)
    args = parser.parse_args()

    # all = print all entries
    # tag = print entries from file
    # file = file to write to
    # empty = main file
    # file = - means stdout

    # key: tag; value: file content for bib file
    # Will be filled with only one tag if all is not given
    tag_dict = {}

    # print(zfn.get_tag_list())
    # print(args.tag)
    # quit()

    if args.all == False and args.tag == None and args.main == False:
        print("You have to either chose a tag or recreate your whole main .bib-file. Please call the help and choose one of the options.")
        quit()


    tmp_string = ""
    tmp_list = []

    # Either print all entries or just the ones associated with the tags.
    total_string = ""
    if args.main:
        output_list = all_entries()
        for i in output_list:
            total_string += i
            total_string += "\n"

    else:
        if args.tag == None:
            tag_list = zfn.get_tag_list()
        else:
            tag_list = [args.tag]

        # entry_list = []
        for e in tag_list:
            output_list = tagged_entries(e)
            tmp_string = ""
            for i in output_list:
                tmp_string += i
                tmp_string += "\n"
            tmp_list.append(tmp_string)


        # print(tmp_list)
        # print(tag_list)

        # quit()
        tag_dict = dict(zip(tag_list, tmp_list))

        total_string = "\n".join(tmp_list)

        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(tag_dict)


    if args.file == None:
        if args.main:
            # Print main bib file
            print("Compiling main bib-file to ", cfg.bibfile_complete)
            # main_file_content = "\n".join(tmp_list)
            main_file_content = total_string
            with open(zfn.correct_home_path(cfg.bibfile_complete), "w") as f:
                f.write(main_file_content)
        else:
            # print tag specific bib file to directory.
            # tag_file_path = cfg.Str_path_bibfolder + args.tag + ".bib"
            # print("Compiling main bib-file to ", tag_file_path)
            # with open(zfn.correct_home_path(tag_file_path), "w") as f:
            #     f.write(tmp_string)
            for tag, file_content in tag_dict.items():
                bibtag_path = cfg.Str_path_bibfolder + tag + ".bib"

                if os.path.isfile(zfn.correct_home_path(bibtag_path)):
                    os.remove(zfn.correct_home_path(bibtag_path))

                with open(zfn.correct_home_path(zfn.correct_home_path(bibtag_path)), "x") as f:
                    f.write(file_content)

    elif args.file == "-":
        # Print to standard out
        print(total_string)
    else:
        # Print to file specified.
        print("Compiling main bib-file to ", args.file)
        if os.path.isfile(args.file):
            with open(zfn.correct_home_path(args.file), "w") as f:
                f.write(total_string)
        else:
            with open(zfn.correct_home_path(args.file), "x") as f:
                f.write(total_string)


if __name__ == "__main__":
    main()
