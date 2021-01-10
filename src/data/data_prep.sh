#!/bin/bash

# Note:
# This is a simplied version for DSC180A Checkpoint #1.
# As a shortened version from auto_phrase.sh, this script only prepares data needed to auto phrase training.
# -- Joey 10/29/2020
# Reference: shangjingbo1226/AutoPhrase (https://github.com/shangjingbo1226/AutoPhrase/blob/master/auto_phrase.sh)

############  Preparing Data ############
# cd /autophrase
# cd ../../

# The comment below are directly from AutoPhrase repo.
# DATA_DIR is the default directory for reading data files.  Because this directory contains not only the default
# dataset, but also language-specific files and "BAD_POS_TAGS.TXT", in most cases it's a bad idea to change it.
# However, when this script is run from a Docker container, it's perfectly fine for the user to mount an external
# directory called "data" and read the corpus from there, since the directory holding the language-specific files
# and "BAD_POS_TAGS.txt" will have been renamed to "default_data".
# if [ -d "default_data" ]; then
#     DATA_DIR=${DATA_DIR:- default_data}
# else
#     DATA_DIR=${DATA_DIR:- data}
#
# fi
echo '      => Running data_prep.sh!'
DATA_DIR=data
# MODEL is the directory in which the resulting model will be saved.
# if [ -d "models" ]; then
#     MODELS_DIR=${MODELS_DIR:- models}
# else
#     MODELS_DIR=${MODELS_DIR:- default_models}
# fi

MODELS_DIR=data/models/
MODEL=${MODEL:- ${MODELS_DIR}/DBLP}


# RAW_TRAIN is the input of AutoPhrase, where each line is a single document.
cp resources/AutoPhrase/data/EN/* ${DATA_DIR}/raw/
cp resources/AutoPhrase/data/BAD_POS_TAGS.txt ${DATA_DIR}/

# DEFAULT_TRAIN=${DATA_DIR}/raw/DBLP.5k.txt
DEFAULT_TRAIN=${DATA_DIR}/raw/DBLP.txt
RAW_TRAIN=${RAW_TRAIN:- $DEFAULT_TRAIN}

green=`tput setaf 2`
reset=`tput sgr0`

mkdir -p tmp
mkdir -p ${MODEL}

if [ $1 == 1 ]; then
    echo ${green}===Downloading Toy Dataset===${reset}
    curl http://dmserv2.cs.illinois.edu/data/DBLP.txt.gz --output ${DEFAULT_TRAIN}.gz
    gzip -d ${DEFAULT_TRAIN}.gz -f
fi
