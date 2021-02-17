from django.shortcuts import render
from django.http import HttpResponse
import os
import json
import pandas as pd
import subprocess
from json import dumps 
from django.views.decorators.csrf import csrf_exempt

if_customized = "true"
selected_doc = ''
selected_pdf = ''
selected_domain = ''
selected_subdomain = ''
selected_keywords = ''
phrases = []

def index(request):
    data = os.listdir('autolibrary/documents')
    data = dumps(data) 
    return render(request, 'autolibrary/index.html', {"data": data})

def result(request):
    data = os.listdir('autolibrary/documents')
    domains = json.load(open('../src/domains_full.json'))
    global selected_doc, selected_pdf
    content = {
        "data": dumps(data), 
        "selected_doc": dumps([selected_doc]), 
        "selected_pdf": dumps([selected_pdf]), 
        "domains": dumps(domains)
    }
    return render(request, 'autolibrary/result.html', content)

def customization(request):
    data = os.listdir('autolibrary/documents')
    domains = json.load(open('../src/domains_full.json'))
    global if_customized, selected_doc, selected_pdf, selected_domain, selected_subdomain, selected_keywords, phrases
    content = {
        "customized": dumps([if_customized]),
        "data": dumps(data), 
        "selected_doc": dumps([selected_doc]), 
        "selected_pdf": dumps([selected_pdf]), 
        "domains": dumps(domains),
        "domain": dumps([selected_domain]),
        "subdomain": dumps([selected_subdomain]),
        "phrases": dumps(phrases),
        "keywords":dumps([selected_keywords]),
    }
    if if_customized == "false":
        if_customized = "true"
    return render(request, 'autolibrary/customization.html', content)

@csrf_exempt
def get_file(request):
    if request.method == 'POST':
        if "file_name" in request.POST:
            global if_customized
            if_customized = "false"
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
            os.system('mkdir -p static/autolibrary/web_scrap')
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
            if selected_domain == '':
                selected_domain = 'ALL'
            if selected_subdomain == '':
                selected_subdomain = 'ALL'
            os.system('mkdir -p ../data/out')
            with open('../data/out/selected_domain.txt', 'w') as fp:
                fp.write(selected_subdomain)
            config = {'fos': [selected_domain]}
            with open('../data/out/fos.json', 'w') as fp:
                json.dump(config, fp)
            # rewrite data-params.json
            config = json.load(open('../config/data-params.json'))
            config['pdfname'] = selected_pdf
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
                # run all targets
                rsh.write('''cd .. \n''')
                rsh.write('''python run.py data \n''')
                rsh.write('''python run.py autophrase \n''')
                rsh.write('''python run.py weight \n''')
                rsh.write('''python run.py webscrape \n''')
                rsh.write('''cp data/out/scraped_AutoPhrase.json website/static/autolibrary/web_scrap/scraped_AutoPhrase.json \n''')
            process = subprocess.Popen(['bash', 'autolibrary/run.sh'])
            process.wait()
            # display phrases with a weighted quality score > 0.5
            global phrases
            data = pd.read_csv('../data/out/weighted_AutoPhrase.csv', index_col = "Unnamed: 0")
            phrases = data[data['score'] > 0.5]['phrase'].to_list()
            return HttpResponse('get domain')
    return HttpResponse('fail to get domain')

@csrf_exempt
def get_keywords(request):  
    if request.method == 'POST':
        if "keywords" in request.POST:
            # save selected keywords to data/out
            global selected_keywords
            selected_keywords = request.POST['keywords']
            config = {'keywords': selected_keywords}
            with open('../data/out/selected_keywords.json', 'w') as fp:
                json.dump(config, fp)
            with open('autolibrary/run.sh', 'w') as rsh:
                # display new webscrape result
                rsh.write('''cd .. \n''')
                rsh.write('''python run.py webscrape \n''')
                rsh.write('''cp data/out/scraped_AutoPhrase.json website/static/autolibrary/web_scrap/scraped_AutoPhrase.json''')
            process = subprocess.Popen(['bash', 'autolibrary/run.sh'])
            process.wait()
            return HttpResponse('get keywords')
    return HttpResponse('fail to get keywords')