from django.shortcuts import render
from django.http import HttpResponse
import os
import json
import time
import subprocess
from json import dumps 
from django.views.decorators.csrf import csrf_exempt

selected_doc = ''
selected_pdf = ''
selected_domain = ''
selected_subdomain = ''
phrases = []

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
    content = {
        "data": data, 
        "selected_doc": file_name, 
        "selected_pdf": pdfname, 
        "domains": domains
    }
    return render(request, 'autolibrary/result.html', content)

def customization(request):
    data = os.listdir('autolibrary/documents')
    domains = json.load(open('../src/domains_full.json'))
    global selected_doc, selected_pdf, selected_domain, selected_subdomain, phrases
    content = {
        "data": dumps(data), 
        "selected_doc": dumps([selected_doc]), 
        "selected_pdf": dumps([selected_pdf]), 
        "domains": dumps(domains),
        "domain": dumps([selected_domain]),
        "subdomain": dumps([selected_subdomain]),
        "phrases": dumps(phrases)
    }
    return render(request, 'autolibrary/customization.html', content)

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
            return HttpResponse('get file')
    return HttpResponse('fail to get file')


@csrf_exempt
def get_domain(request):  
    if request.method == 'POST':
        if "domain" in request.POST:
            # save selected domain to data/out
            global selected_pdf, selected_domain, selected_subdomain
            selected_domain = request.POST['domain']
            selected_subdomain = request.POST['subdomain']
            os.system('mkdir -p ../data/out')
            with open('../data/out/selected_domain.txt', 'w') as fp:
                fp.write(selected_subdomain)
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
            #os.system('bash autolibrary/run.sh')
            process = subprocess.Popen(['bash', 'autolibrary/run.sh'])
            process.wait()
            # time.sleep(20)
            global phrases
            result = open('../data/out/AutoPhrase.txt', 'r')
            lines = result.readlines()
            for line in lines:
                lst = line.split()
                if float(lst[0]) > 0.5:
                    phrase = ''
                    if len(lst) > 2:
                        for p in lst[1:]:
                            phrase += p + ' '
                    else:
                        phrase += lst[1]
                    phrases.append(phrase)
            return HttpResponse('success')
    return HttpResponse('failed')