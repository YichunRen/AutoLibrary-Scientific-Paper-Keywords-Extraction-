from django.shortcuts import render
from django.http import HttpResponse
import os
import json
from json import dumps 
from django.views.decorators.csrf import csrf_exempt

def index(request):
    data = os.listdir('autolibrary/documents')
    data = dumps(data) 
    return render(request, 'autolibrary/index.html', {"data": data})

def askforchild(request):
    data = os.listdir('autolibrary/documents')
    data = dumps(data) 
    global selected_doc, selected_pdf
    file_name = dumps([selected_doc]) 
    pdfname = dumps([selected_pdf])
    domains = json.load(open('../src/domains_full.json'))
    domains = dumps(domains) 
    return render(request, 'autolibrary/result.html', {"data": data, "selected_doc": file_name, "selected_pdf": pdfname, "domains": domains})

selected_doc = ''
selected_pdf = ''

@csrf_exempt
def get_file(request):
    if request.method == 'POST':
        if "file_name" in request.POST:
            # rename document
            file_name = request.POST['file_name']
            pdfname = file_name.replace("'", "")
            pdfname = pdfname.replace(" ", "_")
            os.system('bash autolibrary/rename.sh')
            # save doc name and move to static
            global selected_doc, selected_pdf
            selected_doc = file_name
            selected_pdf = pdfname
            os.system('mkdir -p static/autolibrary/documents')
            command = 'cp autolibrary/documents_copy/' + pdfname + ' static/autolibrary/documents'
            os.system(command)
            return HttpResponse('success')
            
            
            
            # rewrite data-params.json
            # get config indir and outdir ***
            config = {
                "indir": "data/raw",
                "outdir": "data/temp",
                "pdfname": pdfname
            }
            with open('autolibrary/data-params.json', 'w') as fp:
                json.dump(config, fp)
            with open('autolibrary/run.sh', 'w') as rsh:
                # move document to data/raw
                rsh.write('''mkdir -p ../data/raw \n''')
                rsh.write('''cp autolibrary/documents_copy/''')
                rsh.write(pdfname)
                rsh.write(''' ../data/raw \n''')
                # move new data-params.json to config
                rsh.write('''cp autolibrary/data-params.json  ../config \n''')
                rsh.write('''cd .. \n''')
                rsh.write('''python run.py data \n''')
                rsh.write('''python run.py autophrase \n''')
                rsh.write('''python run.py weight \n''')
                rsh.write('''python run.py webscrape \n''')
            os.system('bash autolibrary/run.sh')
            return HttpResponse('success')
    return HttpResponse('FAIL!!!!!')
