#!/usr/bin/env python

import os
import sys
import json

sys.path.insert(0, 'src')
from etl import convert_txt
from model import autophrase
from weight_phrases import change_weight
from webscrape import webscrape
from website import activate_website


def main(targets):
    data_config = json.load(open('config/data-params.json'))
    model_config = json.load(open('config/model-params.json'))
    weight_config = json.load(open('config/weight-params.json'))
    webscrape_config = json.load(open('config/webscrape-params.json'))
    website_config = json.load(open('config/website-params.json'))
    test_config = json.load(open('config/test-params.json'))

    os.system('git submodule update --init')
    # Getting the target
    # If no target is given, then run 'website'
    if len(sys.argv) == 1:
        activate_website(**website_config)
    if 'data' in targets:
        convert_txt(**data_config)
    if 'autophrase' in targets:
        autophrase(data_config['outdir'], data_config['pdfname'], model_config['outdir'], model_config['filename'])
    if 'weight' in targets:
        change_weight(**weight_config)
    if 'webscrape' in targets:
        webscrape(**webscrape_config)
    if 'website' in targets:
        activate_website(**website_config)
    if 'test' in targets:
        convert_txt(test_config['indir'], data_config['outdir'], test_config['pdfname'],)
        autophrase(data_config['outdir'], test_config['pdfname'], model_config['outdir'], model_config['filename'])
        change_weight(**weight_config)
        webscrape(**webscrape_config)
    return

# if __name__ == '__main__':
#     # run via:
#     # python main.py data features model
# targets = sys.argv
main(sys.argv);
