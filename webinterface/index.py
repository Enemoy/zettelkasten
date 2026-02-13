#!/usr/bin/python

import sys
import re
from flask import Flask, render_template, request, redirect, url_for

sys.path.insert(0, '/home/simon/.bin/zettelkasten/')

import main_config as cfg
import main.zettelkasten_functions as zfn



app = Flask(__name__)
@app.route("/")
def index():
    # Index Page with no search term input yet
    options_list = list(set(zfn.get_column_names(cfg.points_tablename) + zfn.get_column_names(cfg.database_bib_sources_tablename)))
    options = {}
    for i in options_list:
        options[i] = i.title()

    options = dict(sorted(options.items()))
    return_list = []


    return render_template('index.html', query="Enter search term!", querytype="Author", options=options, return_list=return_list, table_list=["quote"])

@app.route("/search", methods=['POST'])
def search():
    query = "83"
    querytype = "cid"

    query = request.form['query']
    querytype = request.form['querytype']

    table_list = []

    try:
        table_source = request.form['table_source']
        table_list.append("source")
    except:
        table_source = False

    try:
        table_datapoint = request.form['table_datapoint']
        table_list.append("datapoint")
    except:
        table_datapoint = False

    try:
        table_citation = request.form['table_citation']
        table_list.append("citation")
    except:
        table_citation = False

    # table=3
    query_dict = {querytype: query}
    return_list = []

    options_list = list(set(zfn.get_column_names(cfg.points_tablename) + zfn.get_column_names(cfg.database_bib_sources_tablename)))
    options = {}
    for i in options_list:
        options[i] = i.title()

    options = dict(sorted(options.items()))

    return_list = []
    if query:
        if table_source:
            return_list += zfn.db_select_query(1, query_dict)

        if table_datapoint:
            tmp_list = zfn.db_select_query(2, query_dict)
            for dic in tmp_list:
                dic["content"] = dic["content"].split("\n")
                return_list.append(dic)

        if table_citation:
            tmp_list = zfn.db_select_query(3, query_dict)
            for dic in tmp_list:
                dic["content"] = dic["content"].split("\n")
                return_list.append(dic)

    # Create site with search results
    site = render_template('search.html',
                           query=query,
                           querytype=querytype.title(),
                           options=options,
                           return_list=return_list,
                           table_list=table_list)

    return site


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3124, debug=True)
