#!/usr/bin/python

import random
import main_config as cfg
import zettelkasten_functions as zfn

def main():
    # Cout all rows with quote, generate random number from that, query quote with id.
    count = int(zfn.get_row_count())

    number = random.randrange(0, count)
    query_dict = {'id':str(number)}

    result = zfn.db_select_query(4, query_dict, query_all_bool = False, database = zfn.correct_home_path(cfg.database_file))

    output_string = zfn.pretty_format_citation(result[0])

    print(output_string)

if __name__ == "__main__":
    main()
