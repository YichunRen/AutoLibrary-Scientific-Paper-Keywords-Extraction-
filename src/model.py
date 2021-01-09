import os
import sys
import subprocess

def train_model(outdir, textname, autophrasename):
    # with open ('src/models.sh', 'w') as rsh:
    #     rsh.write("cd AutoPhrase \n")
    #     rsh.write("./auto_phrase.sh")
    
    command = 'cp -r ' + textname + ' AutoPhrase/data/' + autophrasename
    os.system(command)
    
    with open('AutoPhrase/auto_phrase.sh', 'r') as ap:
        head = [next(ap) for x in range(146)]
        
    # Change directory to AutoPhrase and create a new bash
    with open('src/models.sh', 'w') as rsh:
        rsh.write('''cd AutoPhrase \n''')
        
    # Writing the bash to collect data
    with open('src/models.sh', 'a') as rsh:
        for line in head:
            # Replace this line to download DBLP.txt
            if 'RAW_TRAIN=${RAW_TRAIN:- $DEFAULT_TRAIN}' in line:
                rsh.write('''RAW_TRAIN=${DATA_DIR}/${1?Error: no data dir given} \n''')                
                continue
            rsh.write(line)

    # os.system("cd AutoPhrase")
    # os.system("")

    # Run the newly created bash
    # os.system('cd AutoPhrase')
    # os.system("./auto_phrase.sh")
    os.system("bash src/models.sh " + autophrasename)
    # subprocess.call("src/models.sh", shell=True)
    # os.system('cd ../')

    # Make a directory if the target directory does not exist 
    command = 'mkdir -p ' + outdir
    os.system(command)
    
    command = 'cp -r AutoPhrase/models/DBLP/. ' + outdir + ' \n'
    os.system(command)
    return
