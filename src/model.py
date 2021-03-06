import os

def autophrase(unique_key, data_outdir, pdfname, outdir, filename):
    # remove single quotes from file name
    textname = pdfname.replace("'", "")
    textname = textname.replace('.pdf', '_converted.txt')
    textname = textname.replace(' ', '_')
    output_fp = os.path.join(data_outdir, textname)

    # copy txt file to AutoPhrase/test/testdata
    command = 'cp ' + output_fp + ' AutoPhrase' + unique_key + '/test/testdata'
    os.system(command)
    command = 'mv AutoPhrase' + unique_key + '/test/testdata/' + textname + ' AutoPhrase' + unique_key + '/test/testdata/test_raw.txt'
    os.system(command)

    print("\n")
    print(">>>>>>>>>>>>>>>>>>>>>>>> Running AutoPhrase... <<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    print("  => Running AutoPhrase on the input document...")
    # write bash script to call the target test
    with open('src/run' + unique_key + '.sh', 'w') as rsh:
        rsh.write('''cd AutoPhrase'''+ unique_key +''' \n''')
        rsh.write('''/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/AutoPhrase'''+ unique_key +'''/run.py test \n''')
    command = 'bash src/run' + unique_key + '.sh'
    os.system(command)

    # make a directory if outdir does not exist
    outdir += unique_key
    command = 'mkdir -p ' + outdir
    os.system(command)

    # save output
    print("  => Saving results...")
    # filename = 'AutoPhrase' + unique_key + '.txt'
    output_fp = os.path.join(outdir, filename)
    command = 'cp AutoPhrase'+ unique_key +'/data/out/AutoPhrase_Result/AutoPhrase.txt ' + output_fp
    os.system(command)
    print(" => Done! AutoPhrase output is saved as '" + output_fp + "'")
    print("\n")
    return
