# Zettelkasten

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
