# Zettelkasten

In German, "Zettelkasten" means "slip box". It's a place where you can store all your information to create a system of references to connect to one another.

The famous german sociologist Niklas Luhmann used one of these as a litteral locker to store all his references.
I wanted to do the same thing but digitally.
As I am using LaTeX to write my documents, I wanted a system that allows me to use the bibliography managment of LaTeX, while at the same time allowing me to access all the sources and their properties easy via the commandline.
Not only do I want to be able to store all my sources, I also want to store information on what I have read and where to find it as well as specific citations I find relevant without having to remember everything.

------

This repository is a set of script that allow you to:
- Create an SQL-database to store:
	- all your LaTeX-sources in .bib-files
	- citations within from sources
	- datapoints / information from sources
- Convert your .bib-files to entries in the database
- Add citations / information to the database in the terminal or in popup windows
- search the database with the help of dmenu / rofi

The scripts can be used only within the terminal and in standalone mode. A lot of them are also fitted to be used inside of vim to make working with your bibfiles while writing .tex-documents easier.

For example you can:
- choose a citekey with dmenu from the .bibfile you are using in the current document
- look through all citekeys from a certain author while you are in vim with dmenu
- add a citation from the clipboard and the corresponding information to the database

This README.md will expand in time as the repository grows.
Also most of the bash and python scripts have their own help options (-h / --help)


## Functions of zettelkasten

Here is a list of the different functions and their purpose. Of course, there are seperate help for each of the functions, this is just an overview.

### query / search / find

Allows the user to query the different tables in the database.

### convert

Converts .bib-files into entries for the sources table in the database. You can either specify your own folder or or files with the script or give no folders / files as arguments, in case of which the standard folder from the config file will be used.

### compile

Creates prints all entries in sources into a specific file or the terminal without duplicates. This is useful if you want to have one .bib-file with all your entries to cite from.

### backup

Backs up the database to a preconfigured location.

### create / setup

Sets up the database. This means creating the folders with the content files in them, creating the database file and creating the tables in them, all with their respected preconfigured names and locations.

### edit

Allows the user to edit a column of an entry in datapoints or citations by id. Can also be used to edit the content file.

### citekey

Calls a dmenu with the citekeys, either with all of them or a specific search term for a specify collumn.

### delete

Deletes a row with a certain id in either datapoints or citations.

### check

Checks if the citekeys in datapoints and in citations are still in sources.

### change

Script to change all occurences of a citekey in either datapoints or citations. Usefull if a citekey in sources is changed and the sources are recompiled.

### citation

Adds a new citation to the database.

### datapoint

Adds a new datapoint to the database.

### bibfile

Lets the user choose a bibfile with dmenu or rofi and either puts the path into STOUT or the name of the bibfile into the clipboard.

### config

Calls an editor to edit the config file.

### help

The overview over the options.
