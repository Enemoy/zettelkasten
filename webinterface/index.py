#!/usr/bin/python

import sys
import re
from flask import Flask, render_template, request, redirect, url_for

sys.path.insert(0, '/home/simon/.bin/zettelkasten/')

import main_config as cfg
import main.zettelkasten_functions as zfn



app = Flask(__name__)
@app.route("/", methods=['GET'])
def index():
    # Index Page with no search term input yet
    options_list = list(set(zfn.get_column_names(cfg.points_tablename) + zfn.get_column_names(cfg.database_bib_sources_tablename)))
    options = {}
    for i in options_list:
        options[i] = i.title()

    options = dict(sorted(options.items()))
    return_list = []

    return render_template('index.html', query={"Author": "Enter search term!"},  options=options, return_list=return_list, table_list=["citation"])

@app.route("/search", methods=['POST', 'GET'])
def search():
    # Get form values
    query = request.form.getlist('query')
    querytype = request.form.getlist('querytype')

    table_list = request.form.getlist('checkbox_table')
    if len(table_list) == 0:
        table_list.append("citation")

    query_dict = {}

    for q, t in zip(query, querytype):
        if q != "":
            query_dict[t] = q

    print(query_dict)

    return_list = []

    options_list = list(set(zfn.get_column_names(cfg.points_tablename) + zfn.get_column_names(cfg.database_bib_sources_tablename)))
    options = {}
    for i in options_list:
        options[i] = i.title()

    options = dict(sorted(options.items()))

    return_list = []
    if query:
        for t in table_list:

            # Use cid or sid if ID is selected, not the sql index.
            # This is more useful for the end user.
            tmp_query_dict = query_dict
            if "id" in tmp_query_dict:
                id_transformed = query_dict.pop("id")
                if t == "citation" or "datapoint":
                    tmp_query_dict["cid"] = id_transformed
                else:
                    tmp_query_dict["sid"] = id_transformed

            tmp_list = zfn.db_select_query(t, tmp_query_dict)
            for dic in tmp_list:
                # if "content" in dic:
                #     dic["content"] = dic["content"].split("\n")
                return_list.append(dic)

    # Create site with search results
    site = render_template('search.html',
                           query=query_dict,
                           options=options,
                           return_list=return_list,
                           table_list=table_list)

    return site


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3124, debug=True)
