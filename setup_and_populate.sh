#!/bin/bash

# Setup for the database
#

rm bib_sources.db

./create_sources_db.py

./bib_file_converter.py -r
./bib_file_converter.py -d ~/Sync/Dokumente/PDFs/Uni/LaTeX/Bibliografien/Bibs/

exit 0
