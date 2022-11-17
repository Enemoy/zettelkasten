#!/usr/bin/python

import sqlite3
import bib_file_converter
import os
import main_config as cfg

DB_PATH = cfg.database_file.split("/")[-1]

def main():
    HOME = os.path.expanduser( '~' )
    conn = sqlite3.connect(DB_PATH)
    # conn = sqlite3.connect('bib_sources.db')

    c = conn.cursor()

    # for row in c.execute("SELECT journal,title,author,path_to_bibfile FROM sources_collection WHERE path_to_bibfile LIKE '%;%';"):
    #     if row[0] != None:
    #         OUTPUT_STRING = "\"" + row[1] + "\" in the journal: " + row[0]
    #     else:
    #         OUTPUT_STRING = "The entry with the title \"" + row[1] + "\" is in no journal!"

    counter = 0
    for row in c.execute("SELECT title,author,path_to_bibfile FROM sources_collection;"):
        print(row[1])
        counter += 1

    print(counter)
    #     break
    #     TITLE = row[0]
    #     AUTHOR = row[1]
    #     PATH = row[2]
    #     if len(AUTHOR) > 25:
    #         AUTHOR_LIST = AUTHOR.split(" and ")
    #         AUTHOR = AUTHOR_LIST[0] + " et.al."

    #     OUTPUT_STRING = "Occurences of " + TITLE + " (" + AUTHOR + "):"

    #     PATH_LIST = PATH.split(";")
    #     for p in PATH_LIST:
    #         OUTPUT_STRING += "\n\t" + p
    #for row in c.execute("SELECT summary,content,citekey FROM information_collection WHERE path_to_bibfile LIKE '%;%';"):
    # for row in c.execute("SELECT content_path FROM datapoint_collection;"):
    #     print(open(row[0], "r").read())




if __name__ == "__main__":
    main()
