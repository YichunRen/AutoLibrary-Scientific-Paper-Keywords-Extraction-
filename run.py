#!/usr/bin/env python

import os
import sys
import json

sys.path.insert(0, 'src')
from etl import convert_txt
from model import autophrase
from weight_phrases import change_weight

def main(targets):
    data_config = json.load(open('config/data-params.json'))
    model_config = json.load(open('config/model-params.json'))
    weight_config = json.load(open('config/weight-params.json'))
    eda_config = json.load(open('config/eda-params.json'))

    os.system('git submodule update --init')
    
    if 'data' in targets:
        convert_txt(**data_config)
    if 'autophrase' in targets:
        autophrase(data_config['outdir'], data_config['pdfname'], model_config['outdir'], model_config['filename'])
    if 'weight' in targets:
        change_weight(**weight_config)
    
    return

if __name__ == '__main__':
    # run via:
    # python main.py data features model
    targets = sys.argv[1:]
    main(targets)
