#!/usr/bin/env python

import traceback
import os
import glob

# pip install elasticsearch-loader
ELLASTIC_COMMAND = '~/.local/bin/elasticsearch_loader --index cdrs --id-field RECORD_ID csv'


def load_to_elastic(filename, remove_after_loading=False):
    if not filename:
        raise ValueError('No file to load. Please provide the first positional parameter')
    try:
        os.system(f"{ELLASTIC_COMMAND} {filename}")
    except Exception as err:
        print(f'Something was wrong during loading the file {filename} to elasticsearch: {str(err)}')
        print(traceback.format_exc())

    # if remove_after_loading:
    #     remove_file(filename)


if __name__ == '__main__':
    for num, acdr in enumerate(glob.glob('./cdrs/*cdr')):
        load_to_elastic(acdr)
        print(num, acdr)
