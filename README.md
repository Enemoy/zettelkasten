# Zettelkasten

In German, "Zettelkasten" means "slip box". It's a place where you can store all your information to create a system of references to connect to one another.

The famous german sociologist Niklas Luhmann used one of these as a litteral locker to store all his references.
I wanted to do the same thing but digitally.
As I am using LaTeX to write my documents, I wanted a system that allows me to use the bibliography managment of LaTeX, while at the same time allowing me to access all the sources and their properties easy via the commandline.
Not only do I want to be able to store all my sources, I also want to store information on what I have read and where to find it as well as specific citations I find relevant without having to remember everything.

------

## Use Cases

This repository has different use cases:
1. Put all your sources, direct and indirect citations in codeblocks in Emacs Org files (I designed the project around org roam).
2. Collect these sources from you org roam files and put them into the database.
3. Query the database for e.g. "What sources with Friedrich Nietzsche being the author do I have?" (command: zk query -c author -s "Friedrich Nietzsche")
4. Convert all your sources from the database into LaTeX Bibtex files based on the tags.

TODO This manual has to be expanded to fully reveal the full workflow and functionality. This is currently a stub.
