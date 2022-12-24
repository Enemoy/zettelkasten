#!/usr/bin/python

#This script will compile the main-bibliography file and skip duplicates
# Improvement ONE : The script currently only works if the bib-files are properly formatted (lines starting with "@" etc.) This could be done better to find entries based on the actual syntax without being dependend on correct formatting!

import main_config as cfg
import os
import argparse

usage_string="zettelkasten convert [-i INPUT_FOLDER] [-o OUTPUT_FILE]"
description_string="This module will compile all bibliography-files from one folder into one single file without creating any duplicates."
file_help_text="The file you want to compile to. Type \"standard\" to use or standard bib-file."
input_help_text="The input folder containing the bibliography-files."

def create_main_bib(INPUT_FOLDER):
    #creates and returns a list of all entries in the bibfiles in the INPUT_FOLDER
    FILE_LIST = []
    ENTRY_LIST = []
    FILE_LIST = create_file_list(INPUT_FOLDER)
    for file in FILE_LIST:
        #This line checks if the file is a bib-file
        if file.endswith(".bib") or file.endswith(".bibtex"):
            with open(file) as f:
                # Check not for duplicates, but for duplicate citekeys
                for line in f:
                    if line.startswith("@"):
                        temp_string = line
                    elif line.startswith("}"):
                        temp_string += line
                        #check for dublicate
                        if temp_string not in ENTRY_LIST:
                            ENTRY_LIST.append(temp_string)
                    else:
                        temp_string += line

    return ENTRY_LIST

def create_file_list(INPUT_FOLDER):
    #creates and returns a list of all the bib files in the folder
    RETURN_LIST = []
    for root, dirs, files in os.walk(INPUT_FOLDER):
        for file in files:
            RETURN_LIST.append(os.path.join(root, file))

    return RETURN_LIST

def main():
    parser = argparse.ArgumentParser(description=description_string, usage=usage_string, add_help=True)
    parser.add_argument("-o", "--output", type=str, help=file_help_text)
    parser.add_argument("-i", "--input", type=str, help=input_help_text)
    args = parser.parse_args()

    if args.input:
        ARG_INPUT_FOLDER = args.input
    else:
        ARG_INPUT_FOLDER = cfg.Str_path_bibfolder

    if ARG_INPUT_FOLDER.startswith("~"):
        ARG_INPUT_FOLDER = cfg.HOME + ARG_INPUT_FOLDER[1:]

    if args.output == "standard":
        ARG_BIB_FILE = cfg.bibfile_complete
    elif args.output == "terminal" or args.output == None:
        ARG_BIB_FILE = "terminal"
    else:
        ARG_BIB_FILE = args.output

    if ARG_BIB_FILE.startswith("~"):
        ARG_BIB_FILE = cfg.HOME + ARG_BIB_FILE[1:]


    OUTPUT_LIST = create_main_bib(ARG_INPUT_FOLDER)

    if ARG_BIB_FILE != "terminal":
        with open(ARG_BIB_FILE, 'w') as f:
            f.writelines(OUTPUT_LIST)
    else:
        for e in OUTPUT_LIST:
            print(e)

#Main
if __name__ == "__main__":
    main()

