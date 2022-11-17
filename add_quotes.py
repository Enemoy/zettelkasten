#!/usr/bin/python

import os
import sqlite3

# When main is called, this script will add the original citations from the my csv to the database.
# Otherwise the functions will be used to extract the data about a citation from a quote and and it the same way

def main():
    HOME = os.path.expanduser( '~' )
    CSV_FILE_PATH = HOME + "/Sync/Dokumente/PDFs/Uni/LaTeX/Bibliografien/quotes.csv"


    f = open(CSV_FILE_PATH, "r").read()

    content = f.split("\n")

    del content[-1]

    for line in content:
        if line != content[0]:
            columns = line.split("|")
            # print(columns)

            OUTPUT_STRING = "\"" + columns[3] + "\n\t - " + columns[1] + ", S." + columns[2] + "\n"

            if line == content[-1]:
                OUTPUT_STRING = OUTPUT_STRING[0:-1]

            print(OUTPUT_STRING)



if __name__ == "__main__":
    main()
