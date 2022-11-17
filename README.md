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
