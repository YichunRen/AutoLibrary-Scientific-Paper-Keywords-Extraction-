import os
import pdfbox

print("\n")
print(">>>>>>>>>>>>>>>>>>>>>>>> Installing PDFBox... <<<<<<<<<<<<<<<<<<<<<<<<<<<<")
os.system('pip install python-pdfbox')
print("\n")

def convert_txt(outdir, textname):
    print(">>>>>>>>>>>>>>>>>>>>>>>> Converting PDF to TXT... <<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("  => Inputing a pdf document...")
    input_fp = os.path.join(data_fp, text_name)
    p = pdfbox.PDFBox()
    p.extract_text(input_fp)
    
    print("  => Converting to txt...")
    input_txt = input_fp.replace('.pdf', '.txt')
    output_txt = input_txt.replace('.txt', '_converted.txt')
    output = open(output_txt, 'w')
    with open(input_txt, 'rb') as f:
        for line in f:
            if len(line) >= 2 and line[-2] == '-':
                output.write(line.decode()[:-2])
            else:
                output.write(line.decode()[:-1] + ' ')
    output.close()
    print(" => Done! File is saved as '" + output_txt + "'")
    return
