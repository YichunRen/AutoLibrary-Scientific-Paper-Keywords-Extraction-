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
    return HttpResponse('FAIL!!!!!')

domain = ''

@csrf_exempt
def get_domain(request):  
    if request.method == 'POST':
        print('hi')
        if "domain" in request.POST:
            # save selected domain to data/out
            global selected_pdf, domain
            domain = request.POST['domain']
            os.system('mkdir -p ../data/out')
            with open('../data/out/selected_domain.txt', 'w') as fp:
                fp.write(domain)
            # rewrite data-params.json
            reset = False
            config = json.load(open('../config/data-params.json'))
            if config['pdfname'] != selected_pdf:
                config['pdfname'] = selected_pdf
                reset = True
            with open('autolibrary/data-params.json', 'w') as fp:
                json.dump(config, fp)
            with open('autolibrary/run.sh', 'w') as rsh:
                # move selected document to data/raw
                rsh.write('''mkdir -p ../data/raw \n''')
                rsh.write('''cp autolibrary/documents_copy/''')
                rsh.write(selected_pdf)
                rsh.write(''' ../data/raw \n''')
                # move new data-params.json to config
                rsh.write('''cp autolibrary/data-params.json  ../config \n''')
                # reset if switch documents
                if reset:
                    rsh.write('''cd ../AutoPhrase \n''')
                    rsh.write('''python run.py reset \n''')
                # run all targets
                rsh.write('''cd .. \n''')
                rsh.write('''python run.py data \n''')
                rsh.write('''python run.py autophrase \n''')
                rsh.write('''python run.py weight \n''')
                rsh.write('''python run.py webscrape \n''')
            # os.system('bash autolibrary/run.sh')
            return HttpResponse('success')
    return HttpResponse('FAIL!!!!!')
