#!/usr/bin/python

import re
import os
from pathlib import Path
import time
import main_config as cfg
import query_database as qry

def extract_quote_blocks_from_file(path, bool_type):
    with open(path, encoding='utf-8') as f:
        content = f.read()

    if bool_type == "quote":
        REGEX = r'^\#\+BEGIN_SRC\s+quote\s*(.*?)\n(.*?)^\#\+END_SRC'
    else:
        REGEX = r'^\#\+BEGIN_SRC\s+datapoint\s*(.*?)\n(.*?)^\#\+END_SRC'

    pattern = re.compile(REGEX, re.MULTILINE | re.DOTALL)

    # pattern = re.compile(r'^\#\+BEGIN_SRC\s+quote\s*(.*?)\n(.*?)^\#\+END_SRC', re.MULTILINE | re.DOTALL)

    results = []
    for match in pattern.findall(content):
        raw_params, body = match
        # params = dict(re.findall(r':(\w+)\s+"?([^"\s]+)"?', raw_params))

        params = re.findall(r':(\w+)\s+(?:"([^"]+)"|(\S+))', raw_params)

        attributes = {key: val1 if val1 else val2 for key, val1, val2 in params}

        results.append({
            'file': str(path),
            'params': attributes,
            'content': body.strip()
        })

    return results



def main():
    for i in extractor():
        print(i)
        time.sleep(2)


if __name__ == "__main__":
    main()
