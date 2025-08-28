#!/usr/bin/python

import sqlite3
import os
import argparse
import shutil
import sys

sys.path.insert(0, '/home/simon/.bin/zettelkasten/')
import bib_file_converter
import main_config as cfg
import zettelkasten_functions as zfn

# This function will make a backup of the relevant files of the database.
# Use this regularly.
DATBASE_PATH = zfn.correct_home_path(cfg.database_file)
DATBASE_PATH_BACKUP = zfn.correct_home_path(cfg.database_file_backup)
DATAPOINT_DIRECTORY = zfn.correct_home_path(cfg.Str_path_datapoint_directory)
DATAPOINT_DIRECTORY_BACKUP= zfn.correct_home_path(cfg.Str_path_datapoint_directory_backup)
CITATION_DIRECTORY = zfn.correct_home_path(cfg.Str_path_citation_directory)
CITATION_DIRECTORY_BACKUP = zfn.correct_home_path(cfg.Str_path_citation_directory_backup)



def backup_all():

    # backup database
    os.remove(DATBASE_PATH_BACKUP)
    shutil.copy2(DATBASE_PATH, DATBASE_PATH_BACKUP)
    print("Database backed up!")

    if os.path.exists(DATAPOINT_DIRECTORY_BACKUP):
        shutil.rmtree(DATAPOINT_DIRECTORY_BACKUP)
    shutil.copytree(DATAPOINT_DIRECTORY, DATAPOINT_DIRECTORY_BACKUP)
    print("Datapoint directory backed up!")

    if os.path.exists(CITATION_DIRECTORY_BACKUP):
        shutil.rmtree(CITATION_DIRECTORY_BACKUP)
    shutil.copytree(CITATION_DIRECTORY, CITATION_DIRECTORY_BACKUP)
    print("Citation directory backed up!")

    return

def main():
    backup_all()


if __name__ == "__main__":
    main()
