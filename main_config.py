#!/usr/bin/python

# This is the config file for the zettelkasten programm.
# All the relevant variables like paths etc are stored here.
# The config will be imported into python programms to allow access to the variables.
# In case of bash scripts there will be an eval statement at the beginning of this script, which will import the variables to bash scripts as well (see bottom of the script)

import os

# Path to the database-file
database_file = "~/Sync/Dokumente/PDFs/Uni/Zettelkasten/bib_sources.db"

# The path to your main Bibliography, where all entries are stored. (If you want to cite from all you exisiting entires.
bibfile_complete = "~/Sync/Dokumente/PDFs/Uni/LaTeX/Bibliografien/bib_complete.bib"

# Path where all of your .bib files are stored (default variable, can be specified in a lot of cases)
Str_path_bibfolder =  "~/Sync/Dokumente/PDFs/Uni/LaTeX/Bibliografien/Bibs/"

# Path to the directory where all the datapoint contents are stored
Str_path_content_directory = "~/Sync/Dokumente/PDFs/Uni/Zettelkasten/datapoint_files/"

# Path to the directory where all the citations are stored
Str_path_citation_directory = "~/Sync/Dokumente/PDFs/Uni/Zettelkasten/citation_files/"


# Tablename for the collection of your sources.
database_bib_sources_tablename = "sources_collection"

# Tablename for the collection of your datapoints found in the sources.
database_datapoints_tablename = "datapoint_collection"

# Tablename for the collection of all the direct citations you want to save.
database_citations_tablename = "citation_collection"

# Form for the content entry
DATAPOINT_FORM_PATH = "~/.bin/zettelkasten/form_datapoint"
CITATION_FORM_PATH = "~/.bin/zettelkasten/form_citation"

# Terminal you want to use (depending on usage, some commands will be executed with $TERM -e. Here you can choose, which terminal you want to use.
# Example: POPUP_TERMINAL = "urxvt" (the -e flag will be added automatically)
POPUP_TERMINAL = "st -c dialogue_dropdown"

# The command for a dropdown menu you want data to be piped to (has to work dmenu-style
DROPDOWN_MENU = "rofi -theme ~/.config/rofi/theme_wide.rasi -dmenu"

# Backups
database_file_backup = "~/Sync/Dokumente/PDFs/Uni/Zettelkasten_Backup/bib_sources.db"
Str_path_content_directory_backup = "~/Sync/Dokumente/PDFs/Uni/Zettelkasten_Backup/content_files/"
Str_path_citation_directory_backup = "~/Sync/Dokumente/PDFs/Uni/Zettelkasten_Backup/datapoint_files/"


#############################################################################################
#Don't change
all_variables = vars()
HOME = os.path.expanduser( '~' )

#The main body of the config exists to parse the variables of the config file to a bash script.
def main(input_list):
    all_variables = input_list

    for name in all_variables:
        if not name.startswith('__'):
            myvalue = str(eval(name))
            if myvalue == "False":
                myvalue = "0"
            elif myvalue == "True":
                myvalue = "1"
            print("export " + name + "=\"" + myvalue + "\"")

if __name__ == "__main__":
    main(all_variables)

