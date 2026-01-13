#!/usr/bin/python

# This is the config file for the zettelkasten programm.
# All the relevant variables like paths etc are stored here.
# The config will be imported into python programms to allow access to the variables.
# In case of bash scripts there will be an eval statement at the beginning of this script, which will import the variables to bash scripts as well (see bottom of the script)

import os

# Path to the database-file
database_file = "~/.local/zettelkasten/zettelkasten.db"

# The path to your main Bibliography, where all entries are stored. (If you want to cite from all you exisiting entires.
bibfile_complete = "~/.local/zettelkasten/sources_full.bib"

# Path where all of your .bib files are stored (default variable, can be specified in a lot of cases)
Str_path_bibfolder =  "~/.local/zettelkasten/latex_sources/"

# Tablename for the collection of all the direct citations you want to save.
database_citations_tablename = "citation_collection"

# new table name after doom emacs integration
points_tablename = "points_collection"

# Terminal you want to use (depending on usage, some commands will be executed with $TERM -e. Here you can choose, which terminal you want to use.
# Example: POPUP_TERMINAL = "urxvt" (the -e flag will be added automatically)
POPUP_TERMINAL = "kitty --class dropdown_dialog"

# The command for a dropdown menu you want data to be piped to (has to work dmenu-style
DROPDOWN_MENU = "wofi -w 2 -M fuzzy --dmenu -i -W 1300"



# Backups
database_file_backup = "~/.local/zettelkasten/backup/zettelkasten.db"

# Path to sourcecode
Str_path_sourcecode = "~/.bin/zettelkasten/"
Str_path_sourcecode_main="main/"
Str_path_sourcecode_scripts="scripts/"
Str_path_sourcecode_snippets="snippets/"

# The path to your org roam files, should be identical to the 'org-roam-directory' variable in your doom / emacs config.
Org_roam_dir="~/.local/roam/"

# Generic Testfiles, if you want to have one central file for quotes and datapoints
Org_roam_quotes=""
Org_roam_datapoints=""


#############################################################################################
#Don't change
all_variables = vars()
HOME = os.path.expanduser( '~' )

if Str_path_sourcecode.startswith("~"):
    Str_path_sourcecode = HOME + Str_path_sourcecode[1:]

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
            elif myvalue.startswith("~"):
                #if os.isfile(myvalue) or os.ispath(myvalue):
                myvalue = HOME + myvalue[1:]
            print("export " + name + "=\"" + myvalue + "\"")

if __name__ == "__main__":
    main(all_variables)

