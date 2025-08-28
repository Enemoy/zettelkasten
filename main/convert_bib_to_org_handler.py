#!/usr/bin/python

import argparse
import sys

sys.path.insert(0, '/home/simon/.bin/zettelkasten/')
import main_config as cfg
import bib_file_converter
import zettelkasten_functions as zfn
import create_database as crt

Str_manual_description="Opens the input file (must be with biblatex content) and converts it to an org source codeblock."
Str_manual_usage="zettelkasten org_convert [-h/--help]"
Str_manual_input="The input string, that should be converted."

def main():
    parser = argparse.ArgumentParser(description=Str_manual_description, usage=Str_manual_usage, add_help=True)
    parser.add_argument("file", type=str, help=Str_manual_input)
    args = parser.parse_args()

    # print(args.file)

    if zfn.check_file_exists(args.file):
        source_dict = zfn.create_entry_list(args.file)

        output_string = zfn.convert_to_org_source(source_dict)

        print(output_string)

    else:
        print("Warning, not a file!")
        quit()



if __name__ == "__main__":
    main()
