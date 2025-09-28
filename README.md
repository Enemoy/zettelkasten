# Zettelkasten

In German, "Zettelkasten" means "slip box". It's a place where you can store all your information to create a system of references to connect to one another.

The famous german sociologist Niklas Luhmann used one of these as a litteral locker to store all his references.
I wanted to do the same thing but digitally.
As I am using LaTeX to write my documents, I wanted a system that allows me to use the bibliography managment of LaTeX, while at the same time allowing me to access all the sources and their properties easy via the commandline.
Not only do I want to be able to store all my sources, I also want to store information on what I have read and where to find it as well as specific citations I find relevant without having to remember everything.

----

## TODO

The code for this program or better said plugin / extension is still a work in progress.
Here are some general future plans:
- better, more straight forward documentation
- a deploy / setup script that sets up all paths and directories inside the system so that the user has to do as few adjustments as possible
- upload of snippets

------
## Purpose

There are many citiation software projects out there and there are many stable note taking systems (e.g. Obisidian) that work around a markup language like markdown.
So why this one, why was it created?

The purpose of the program is to create an enviroment **around** Doom Emacs and Org Roam (UI), that allows safe storage of sources and citations (direct or indirect) in a seperate system, that is independant of Emacs.
This means, that notes inside of your org-roam files can be taken, created, deleted, edited and whatever else you do with it.
All the sources you want to track are stored inside of these org files in the form of codeblocks.
**This program then simply extracts all this data from said codeblocks and transfers them into a seperate database.**
On the one hand, this design has the advantage of still working, even if your Emacs crashes.
You basically check in all the new entries you have at regular intervals (cronjob, manual script-triggering, whatever you like).

You can then query the database in the terminal, here's an example:

`zk query -c author -s "Friedrich Nietzsche" -o title`

This command will query the database for all books by Friedrich Nietzsche and output their title.

## Basic notions

Before presenting the different commands, here are some notions that are used throughout the project:
- **"zk"**: means Zettelkasten, an abbreviation for this program.
- **"source"** means a literal source of something, like a book, scientific article or a chapter in a book
- **"quote"**: A literal citation in a source.
- **"datapoint"**: In indirect citation in a source.
- **"tables"**: There are four callable tables in the database (acutally only two). You can access them when querying the database with the `-t <Number>` option:
	- **1**: The sources table, where all your books, articles etc. are stored.
	- **2**: Queries only the datapoints.
	- **3**: Queries only the quotes.
	- **4**: Queries datapoints as well as quotes.

## Codeblocks

Here are examples of codeblocks that are used inside of org files and will be found by the converter.

Here is an entry for a book:
```
#+BEGIN_SRC source :citekey antioedipus1972 :type book
author = Gilles Deleuze and Félix Guattari
title = Anti-Ödipus - Kapitalismus und Shizophrenie I
year = 2021
publisher = Suhrkamp
address = Frankfurt
edition = 17
origdate = 1972
tags = postmoderne,klassiker
#+END_SRC
```

Here is a direct citation (quote) by Deleuze:
```
#+BEGIN_SRC quote :citekey antioedipus1972 :page "39" :note "Unterdrückung, Heil"
Warum kämpfen die Menschen für ihre Knechtschaft als ginge es um ihr Heil?
#+END_SRC
```


Here is an indirect quote (datapoint) by Deleuze:
```
#+BEGIN_SRC datapoint :citekey antioedipus1972 :page "39" :note "Unterdrückung, Heil"
In this paragraph, Deleuze goes after the question why people are drawn to ideologies like Fascism that oppress them and meanwhile think they are being freed.
#+END_SRC
```
Here is an entry for an article:
```
#+BEGIN_SRC source :citekey disciplinedhaslanger2019 :type article
author = , Sally Haslanger
title = Disciplined Bodies and Ideology Critique
year = 2019
journal = Glass Bead
volume = 2
number = 1
tags = analytic
#+END_SRC
```

## Workflow

How do you use the program?

1. Write notes inside your emacs org-roam files (or just general org-files, they just have to be in one central directory).
2. Add your sources in the form of codeblocks (there are snippets for yas inside this project). Give each source a citekey (it will later be used in LaTeX) and the relevant data. You can put any source anywhere in the files, the location will be safed to the database. Also add tags to your sources to give them topics.
3. Add quotes and datapoints in the same manner. Add the citekeys from the sources to their codeblock as they will later be used to relate sources to citations.
4. Let the programm scan all your files (`zk compile`)
5. After adding all the content to the database, either use it to find information or create bibfiles for LaTeX from all your sources (`zk bibfile -a` or `zk bibfile -m`). They will be autogenerated from your database. For each tag (or a specific one) a bibfile will be created, containing all related source entries.
6. Use your bibfiles to write LaTeX documents. I personally don't do that in Emacs, but do whatever you like.

This project also contains a lot of helper scripts that allow easier access and conversion of types and files, e.g.:
- `dmenu`-scripts (or use wofi or whatever, there is a variable for chosing a menu inside the config) to (these will be documented better in the future):
	- search citekeys or titles and put them into the clipboard
	- to convert bibfiles in your Download dir to source entries for this program

## Documentation and examples

I am trying to properly document this project and gave every subprogram a help function.
In the repo, there is the main bash script that triggers these smaller programs and relays their arguments to them.

Here are examples for how to use the program:

This command checks for all sources that have "Friedrich Nietzsche" in their author field.
```
zk query -c author -s "Friedrich Nietzsche"
```

This command checks for all quotes or datapoints that have "Friedrich Nietzsche" as their author, based on their related source.
```
zk query -c author -s "Friedrich Nietzsche" -t 4
```

This command checks for all sources that have the publisher "Bloomsbury" and have been released in the year 2025 and outputs only their authors:
```
zk query -c publisher -s "Bloomsbury" -c year -s 2025 -o author
```

This command collects all your sources and citations from the org files and puts them into the database:
```
zk compile
```

This command creates one single Biblatex file (`.bib`) that contains all your sources:
```
zk bibfile -m
```

This command creates one Biblatex file (`.bib`) that contains all sources with the tag "Psychoanalyse" into an output file of the same name:
```
zk bibfile -t Psychoanalyse -f Psychoanalyse.bib
```
## Project Structure

There are several directories with code inside this repo.

### Main

Here is the main codebase, e.g. the source code for databse-setup, queries, the main functions of the program, file converters etc.

### Scripts

In this directory are all the scripts that are supposed to ease your access to the database through e.g. dmenu-scripts.
I use them to access e.g. citekeys out of vim while editing LaTeX or paste bibfiles I download to the clipboard as org-compatible codeblocks.
The scripts are supposed to fluently use the program with hotkeys from your system (you have to configure those in some way).

### Snippets

Inside the project, there are several snippets to safe you time in writing the codeblocks yourself.
They can be used to either automatically create source or a citation.
If you create a citation, the snippet will use a dmenu-script to ask for the citekey.
This will be useful, if you already have a lot of sources and wish to find their exact citekey, but only know the title of the source.

Also, you can find excerpts from my configs for different programs / enviroments that I use to configure hotkeys that call the scripts in my system.

They are just examples though and depend on the enviroment you use.
I tried to give them useful descriptions so you can easily implement them to your liking.
