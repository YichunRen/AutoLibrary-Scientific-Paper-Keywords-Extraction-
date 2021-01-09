#!/usr/bin/env python

import sys
import os
import json

sys.path.insert(0, 'src')

from etl import get_data
from model import train_model
from eda import generate_report_data
from phrasal_segmentation import segment
from phrasal_segmentation import move_annotated_result
from utils import convert_eda
from utils import convert_report

def main(targets):
    data_config = json.load(open('config/data-params.json'))
    model_config = json.load(open('config/model-params.json'))
    eda_config = json.load(open('config/eda-params.json'))

    os.system('git submodule update --init')
    
    if 'data' in targets:
        get_data(data_config['outdir'], data_config['textname'], False)
    if 'model' in targets:
        train_model(**model_config)
    if 'eda' in targets:
        print("===Generating EDA===")
        generate_report_data(data_config["outdir"], eda_config['text_name'], eda_config["outdir"])	
        convert_eda(**eda_config)
    if 'segment' in targets:
        segment(**model_config)
        move_annotated_result(False)
        convert_report(**eda_config)
    if 'all' in targets:
        get_data(data_config['outdir'], data_config['textname'], False)
        train_model(**model_config)
        print("===Generating EDA===")
        generate_report_data(data_config["outdir"], eda_config['text_name'], eda_config["outdir"])
        convert_eda(**eda_config)
        segment(**model_config)
        move_annotated_result(False)
        convert_report(**eda_config)
    if 'test' in targets:
        get_data(data_config['outdir'], data_config['textname'], True)
        train_model(model_config['outdir'], "test/testdata/test.txt", "EN/test.txt")
        print("===Generating EDA===")
        generate_report_data("test/testdata", "test.txt", eda_config["outdir"])
        convert_eda(**eda_config)
        segment(model_config['outdir'], "test/testdata/test.txt", "EN/test.txt")
        move_annotated_result(True)
        convert_report(**eda_config)
        
    return

if __name__ == '__main__':
    # run via:
    # python main.py data features model
    targets = sys.argv[1:]
    main(targets)
