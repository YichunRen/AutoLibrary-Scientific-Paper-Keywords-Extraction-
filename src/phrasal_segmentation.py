import os
import sys
import subprocess
import re
import gensim

def segment(outdir, textname, autophrasename):
    command = 'cp -r ' + textname + ' AutoPhrase/data/' + autophrasename
    os.system(command)
    
    with open('AutoPhrase/phrasal_segmentation.sh', 'r') as ap:
        head = [next(ap) for x in range(89)]
        
    # Change directory to AutoPhrase and create a new bash
    with open('src/phrasal_segmentation.sh', 'w') as rsh:
        rsh.write('''cd AutoPhrase \n''')
        
    # Writing the bash to collect data
    with open('src/phrasal_segmentation.sh', 'a') as rsh:
        for line in head:
            # Replace this line to download DBLP.txt
            if 'TEXT_TO_SEG=${TEXT_TO_SEG:- ${DATA_DIR}/EN/DBLP.5K.txt}' in line:
                rsh.write('''TEXT_TO_SEG=${TEXT_TO_SEG:- ${DATA_DIR}/${1?Error: no data dir given}} \n''')
                continue
            rsh.write(line)

    # Run the newly created bash
    os.system("bash src/phrasal_segmentation.sh " + autophrasename)
    command = 'cp -r AutoPhrase/models/DBLP/. ' + outdir + ' \n'
    os.system(command)

    # Train Word2Vec model on phrasal segmentation results
    print("===Converting Phrasal Segmentation Results===")
    convert_text = []
    with open(os.path.join(outdir, 'segmentation.txt'), 'r') as text:
        for line in text:  
            if line == '\n' or line == '.\n':
                continue
                
            lst = []
            line = line.lower()
            if line[-1] == '\n':
                line = line[:-1]
                
            to_convert = re.findall(r'<phrase>(.+?)</phrase>', line)
            for phrase in re.split(r'<phrase>(.+?)</phrase>', line):
                if len(phrase.split()) > 1 and phrase in to_convert:
                    lst.append('_'.join(phrase.split()))
                elif phrase not in ['', ' ']:
                    for p in phrase.split():
                        lst.append(p)

            convert_text.append(lst)

    print("===Training Word2Vec===")
    model = gensim.models.Word2Vec(convert_text)
    #model.train(convert_text, total_examples=len(convert_text), epochs=10)
    os.system('mkdir -p data/report')
    model.save("data/report/word2vec.model")
    return

def move_annotated_result(if_test):
    if if_test:
        os.system('cp test/testdata/test_multi-words.csv references/annotated_multi-words.csv \n')
    else:
        os.system('cp references/sub_multi-words.csv references/annotated_multi-words.csv \n')
    return
