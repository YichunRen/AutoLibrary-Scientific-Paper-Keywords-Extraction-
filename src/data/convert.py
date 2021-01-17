import os
import pdfbox

print("\n")
print(">>>>>>>>>>>>>>>>>>>>>>>> Installing PDFBox... <<<<<<<<<<<<<<<<<<<<<<<<<<<<")
os.system('pip install python-pdfbox')
print("\n")

def convert_txt(indir, outdir, pdfname):
    print(">>>>>>>>>>>>>>>>>>>>>>>> Converting PDF to TXT... <<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("  => Inputing a pdf document...")
    input_fp = os.path.join(indir, pdfname)
    temp_txt = input_fp.replace('.pdf', '.txt')
    temp_txt = temp_txt.replace(' ', '_')
    p = pdfbox.PDFBox()
    p.extract_text(input_fp, temp_txt)
    
    command = 'mkdir -p ' + outdir
    os.system(command)
    
    print("  => Converting to txt...")
    textname = pdfname.replace('.pdf', '_converted.txt')
    output_fp = os.path.join(outdir, textname)
    output_txt = open(output_fp, 'w')
    with open(temp_txt, 'rb') as f:
        for line in f:
            if len(line) >= 2 and line[-2] == '-':
                output_txt.write(line.decode()[:-2])
            else:
                output_txt.write(line.decode()[:-1] + ' ')
    output_txt.close()
    
    command = 'rm ' + temp_txt
    os.system(command)
    print(" => Done! File is saved as '" + output_fp + "'")
    return
