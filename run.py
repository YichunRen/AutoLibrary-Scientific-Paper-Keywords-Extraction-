#!/usr/bin/env python

import sys
import os
import json

sys.path.insert(0, 'src/data')
from convert import convert_txt

def main(targets):
    data_config = json.load(open('config/data-params.json'))
    model_config = json.load(open('config/model-params.json'))
    eda_config = json.load(open('config/eda-params.json'))

    os.system('git submodule update --init')
    
    if 'data' in targets:
        convert_txt(**data_config)

    return

if __name__ == '__main__':
    # run via:
    # python main.py data features model
    targets = sys.argv[1:]
    main(targets)
