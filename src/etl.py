import os
import sys
import json

# This file downloads DBLP.txt dataset

def get_data(outdir, textname, if_test):
    # Read the first few lines of the original AutoPhrase bash for getting data
    with open('AutoPhrase/auto_phrase.sh', 'r') as ap:
        head = [next(ap) for x in range(61)]
        
    # Change directory to AutoPhrase and create a new bash
    with open('src/run.sh', 'w') as rsh:
        rsh.write('''cd AutoPhrase \n''')

    # Writing the bash to collect data
    with open('src/run.sh', 'a') as rsh:
        for line in head:
            if if_test:
                # If target is test, change the input file of AutoPhrase 
                if 'RAW_TRAIN=' in line:
                    rsh.write('''RAW_TRAIN=${DATA_DIR}/EN/test.txt \n''')
                else:
                    rsh.write(line)
            else:
                # Replace this line to download DBLP.txt
                if 'DBLP.5K' in line:
                    rsh.write('''DEFAULT_TRAIN=${DATA_DIR}/EN/DBLP.txt \n''')
                else:
                    rsh.write(line)

    # Make a directory if the target directory does not exist
    command = 'mkdir -p ' + outdir
    os.system(command)
    
    # Run the newly created bash
    os.system("bash src/run.sh")

    # Move the data to our data folder
    os.system('cd ../')
    command = 'cp -r AutoPhrase/data/EN/. ' + outdir + ' \n'
    os.system(command)
    return
