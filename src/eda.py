import os
from collections import defaultdict
import re
import json

# This file performs EDA

def generate_report_data(data_fp, text_name, outdir):       
    n_document = 0
    n_sentence = 0
    n_token = 0
    document_len = []
    sentence_len = []
    all_token = defaultdict(int)
    is_title = True
    
    with open(os.path.join(data_fp, text_name), 'r') as text:
        for line in text: 
            if line == '.\n' or line == '\n':
                continue

            next_line = next(text, None)
            # the current line is a title
            if next_line == '.\n': 
                n_document += 1
                is_title = True
            # the current line is an abstract
            elif next_line == '\n': 
                is_title = False

            # split lines into sentences by .?!
            s_lst = re.split('\.\s|\?\s|\!\s|\.|\?|\!', line)
            n_sentence += len(s_lst)

            for s in s_lst:
                # remove capitalization
                s = s.lower()
                # split sentences into tokens by whitespace and ,:;
                t_lst = s.split()
                t_lst = [x[:-1] if x[-1] in [',', ':', ';'] else x for x in s]
                # tokenize the text
                t_lst = ''.join(s).strip().split()
                n_token += len(t_lst)
                if is_title:
                    document_len.append(len(t_lst))
                else:
                    document_len[-1] += len(t_lst)
                sentence_len.append(len(t_lst))
                for t in t_lst:
                    all_token[t] += 1
    n_unique = len(all_token)

    count_white = 0
    weird = []
    with open(os.path.join(data_fp, text_name), 'r') as text:
        for line in text: 
            if line == '.\n' or line == '\n':
                continue

            # find consecutive whitespace
            count_white = 0
            spaces = list(re.findall("\s{2}", line))
            if len(spaces) > 0:
                count_white += 1

            # find words with "weird" characters
            found = False
            line = ' '.join(re.split('\.\s|\?\s|\!\s|\.|\?|\!', line))
            words = line.split()
            for word in words:
                for c in word:
                    if c in '#$\*+<=>@\^_`|~' and not found:  
                        weird.append(word)
                        found = True
                found = False

    # Make a directory if the target directory does not exist 
    command = 'mkdir -p ' + outdir
    os.system(command)

    # write results to files
    with open(os.path.join(outdir, 'report_data.txt'), 'w') as f:
        f.write(str(n_document) + '\n')
        f.write(str(n_sentence) + '\n')
        f.write(str(n_token) + '\n')
        f.write(str(n_unique) + '\n')
        f.write(str(document_len) + '\n')
        f.write(str(sentence_len) + '\n')
        f.write(str(count_white) + '\n')
        f.write(str(weird))
        f.close()
    
    json.dump(all_token, open(os.path.join(outdir, 'report_tokens.csv'), 'w'))
    return
