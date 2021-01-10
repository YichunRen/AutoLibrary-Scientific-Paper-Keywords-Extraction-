import pandas as pd
import numpy as np
from tqdm import tqdm # Visualization of loop progress
import os
from os import listdir
import pandas as pd
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt
import re
from gensim.models import Word2Vec
import pickle
#ignore future warning because of different versions in the environment
import warnings
warnings.filterwarnings("ignore") 

def search_single_line(line):
    if '<phrase>' in line:
        curr_phrases = []
        for i in line.split('<phrase>'):
            if i.strip() == '':
                continue
            first = True
            for ph in i.split('</phrase>'):
                if first:
                    curr_phrases.append('_'.join(ph.split()))
                    first = False
                else:
                    for w in ph.split():
                        curr_phrases.append(w.strip())
        return curr_phrases
    else:
        return line.split()

def generate_model(outerdir, outdir,**kwargs):
    os.makedirs(outerdir, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    
    out_file_dir = 'data/out/AutoPhrase_Result/'
    result = open(out_file_dir + 'segmentation.txt', 'r')
    counter = 0
    all_sents = []
    for line in result:
        if line.strip() == '' or line.strip() == '.':
            continue
        all_sents.append(search_single_line(line))
        
    print(' => Generating model for report')
    #model = Word2Vec(all_sents, min_count = 5, size = 50, workers = 2, window = 5, sg = 0)
    model = Word2Vec(all_sents)
    #model.train(all_sents, total_examples=len(all_sents))
    model.save( outdir + "/word2vec.model")
    print(" => Done! Model is saved in data/report/report_files")      
    return

