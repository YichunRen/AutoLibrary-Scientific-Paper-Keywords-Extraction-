from django.shortcuts import render
from django.http import HttpResponse
import os
import json
import pandas as pd
import subprocess
from json import dumps
from django.views.decorators.csrf import csrf_exempt
import urllib.request as urllib2
from werkzeug.utils import secure_filename

# if_customized = "true"
# selected_doc = ''
# selected_pdf = ''
# selected_domain = ''
# selected_subdomain = ''
# selected_keywords = ''
# phrases = []

def index(request):

    unique_key = request.session.session_key
    os.system('mkdir -p autolibrary/documents/' + unique_key )
    os.system('cp autolibrary/documents/* ' + 'autolibrary/documents/' + unique_key)
    data = os.listdir('autolibrary/documents/' + unique_key)
    data = dumps(data)
    shared_obj = request.session.get('myobj',{})
    shared_obj['selected_doc'] = ''
    shared_obj['selected_pdf'] = ''
    shared_obj['if_customized'] = "true"
    shared_obj['selected_domain'] = ''
    shared_obj['selected_subdomain'] = ''
    shared_obj['selected_keywords'] = ''
    shared_obj['phrases'] = []

    request.session['myobj'] = shared_obj
    return render(request, 'autolibrary/index.html', {"data": data})

def result(request):
    unique_key = request.session.session_key
    data = os.listdir('autolibrary/documents/' + unique_key)
    domains = json.load(open('../src/domains_full.json'))
    #global selected_doc, selected_pdf
    #new
    shared_obj = request.session['myobj']
    selected_doc = shared_obj['selected_doc']
    selected_pdf = shared_obj['selected_pdf']

    content = {
        "data": dumps(data),
        "selected_doc": dumps([selected_doc]),
        "selected_pdf": dumps([selected_pdf]),
        "domains": dumps(domains)
    }
    return render(request, 'autolibrary/result.html', content)

def customization(request):
    unique_key = request.session.session_key
    data = os.listdir('autolibrary/documents/' + unique_key)
    domains = json.load(open('../src/domains_full.json'))

    #global if_customized, selected_doc, selected_pdf, selected_domain, selected_subdomain, selected_keywords, phrases
    #new
    shared_obj = request.session['myobj']
    #global selected_doc, selected_pdf
    if_customized = shared_obj['if_customized']
    selected_pdf = shared_obj['selected_pdf']
    selected_doc = shared_obj['selected_doc']
    selected_domain = shared_obj['selected_domain']
    selected_subdomain = shared_obj['selected_subdomain']
    selected_keywords = shared_obj['selected_keywords']
    phrases = shared_obj['phrases']

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
        shared_obj['if_customized'] = if_customized

    request.session['myobj'] = shared_obj
    return render(request, 'autolibrary/customization.html', content)

@csrf_exempt
def get_file(request):
    unique_key = request.session.session_key
    if request.method == 'POST':
        shared_obj = request.session['myobj']

        if "file_name" in request.POST:
            #global if_customized
            if_customized = "false"
            shared_obj['if_customized'] = if_customized

            # rename document
            file_name = request.POST['file_name']
            pdfname = file_name.replace("'", "")
            pdfname = pdfname.replace(" ", "_")
            os.system('bash autolibrary/rename.sh')
            # save doc name and move to static
            #global selected_doc, selected_pdf
            selected_doc = file_name
            selected_pdf = pdfname
            shared_obj['selected_pdf'] = selected_pdf
            shared_obj['selected_doc'] = selected_doc

            os.system('mkdir -p static/autolibrary/documents')
            os.system('mkdir -p static/autolibrary/web_scrap')
            command = 'cp autolibrary/documents/' + unique_key + '/' + file_name + ' autolibrary/documents_copy/' + unique_key
            os.system(command)
            command = 'cp autolibrary/documents_copy/' + unique_key + '/' + file_name + ' static/autolibrary/documents'
            os.system(command)

            request.session['myobj'] = shared_obj
            return HttpResponse('get file')

    request.session['myobj'] = shared_obj
    return HttpResponse('fail to get file')

@csrf_exempt
def get_domain(request):
    shared_obj = request.session['myobj']

    if request.method == 'POST':
        if "domain" in request.POST:
            # save selected domain to data/out
            #global selected_pdf, selected_domain, selected_subdomain
            #global selected_pdf, selected_domain, selected_subdomain
            selected_domain = request.POST['domain']
            selected_subdomain = request.POST['subdomain']
            selected_pdf = shared_obj['selected_pdf']
            if selected_domain == '':
                selected_domain = 'ALL'
            if selected_subdomain == '':
                selected_subdomain = 'ALL'

            shared_obj['selected_domain'] = selected_domain
            shared_obj['selected_subdomain'] = selected_subdomain

            os.system('mkdir -p ../data/out')

            unique_key = request.session.session_key
            with open('../data/out/selected_domain_' + unique_key + '.txt', 'w') as fp:
                fp.write(selected_subdomain)
            config = {'fos': [selected_domain]}
            with open('../data/out/fos_' + unique_key + '.json', 'w') as fp:
                json.dump(config, fp)
            # rewrite data-params.json
            config = json.load(open('../config/data-params.json'))
            config['pdfname'] = selected_pdf
            with open('autolibrary/data-params.json', 'w') as fp:
                json.dump(config, fp)





            # add timestamp
            import datetime
            timestamp = request.session.get('timestamp')
            timestamp = datetime.datetime.now(datetime.timezone.utc)
            print(timestamp)
            request.session['timestamp'] = timestamp
            current = request.session.session_key
            # find all sessions
            from django.contrib.sessions.models import Session
            from django.utils import timezone
            from django.contrib.sessions.backends.db import SessionStore
            sessions = Session.objects.filter(expire_date__gte=timezone.now())
            sessions_in_queue = []
            for session in sessions:
                if session.session_key != current and session['in_queue'] == "true":
                    sessions_in_queue.append(session['timestamp'])
            sessions_in_queue.sort()




            with open('autolibrary/run.sh', 'w') as rsh:
                # move selected document to data/raw
                rsh.write('''mkdir -p ../data/raw \n''')
                rsh.write('''cp autolibrary/documents_copy/''')
                rsh.write(selected_pdf)
                rsh.write(''' ../data/raw \n''')
                # move new data-params.json to config
                rsh.write('''cp autolibrary/data-params.json  ../config \n''')
                rsh.write('''cd .. \n''')
                rsh.write('''/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py data \n''')
                rsh.write('''/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py autophrase \n''')
                rsh.write('''mkdir test_weight \n''')
                rsh.write('''/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py weight ''' + unique_key +  ''' \n''')
                rsh.write('''mkdir test_webscrape \n''')
                rsh.write('''/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py webscrape ''' + unique_key +  ''' \n''')
                rsh.write('''cp data/out/scraped_AutoPhrase.json website/static/autolibrary/web_scrap/scraped_AutoPhrase.json \n''')
                rsh.write('''mkdir test_end \n''')


            process1 = subprocess.Popen(['bash', 'autolibrary/run.sh'])
            process1.wait()

            # display phrases with a weighted quality score > 0.5
            #global phrases
            data = pd.read_csv('../data/out/weighted_AutoPhrase.csv', index_col = "Unnamed: 0")
            phrases = data[data['score'] > 0.5]['phrase'].to_list()
            shared_obj['phrases'] = phrases

            request.session['myobj'] = shared_obj
            return HttpResponse('get domain')
    request.session['myobj'] = shared_obj
    return HttpResponse('fail to get domain')

@csrf_exempt
def get_keywords(request):
    shared_obj = request.session['myobj']
    if request.method == 'POST':
        if "keywords" in request.POST:
            # save selected keywords to data/out
            #global selected_keywords
            selected_keywords = request.POST['keywords']
            shared_obj['selected_keywords'] = selected_keywords
            config = {'keywords': selected_keywords}
            with open('../data/out/selected_keywords.json', 'w') as fp:
                json.dump(config, fp)
            with open('autolibrary/run.sh', 'w') as rsh:
                # display new webscrape result
                rsh.write('''cd .. \n''')
                rsh.write('''/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py webscrape \n''')
                rsh.write('''cp data/out/scraped_AutoPhrase.json website/static/autolibrary/web_scrap/scraped_AutoPhrase.json''')
            process = subprocess.Popen(['bash', 'autolibrary/run.sh'])
            process.wait()
            request.session['myobj'] = shared_obj
            return HttpResponse('get keywords')
    request.session['myobj'] = shared_obj
    return HttpResponse('fail to get keywords')

@csrf_exempt
def get_url(request):
    unique_key = request.session.session_key
    shared_obj = request.session['myobj']
    if request.method == 'POST':
        if "url" in request.POST:
            download_url = request.POST['url']
            pdfname = download_url.split('/')[-1]
            response = urllib2.urlopen(download_url)

            os.system('mkdir -p autolibrary/documents/' + unique_key )
            os.system('mkdir -p autolibrary/documents_copy/' + unique_key )

            fp = "autolibrary/documents/" + unique_key + '/' + pdfname
            file = open(fp, 'wb')
            file.write(response.read())
            file.close()
            #global if_customized
            if_customized = "false"
            shared_obj['if_customized'] = if_customized
            #global selected_doc, selected_pdf
            selected_doc = pdfname
            selected_pdf = pdfname
            shared_obj['selected_doc'] = selected_doc
            shared_obj['selected_pdf'] = selected_pdf

            os.system('mkdir -p static/autolibrary/documents')
            os.system('mkdir -p static/autolibrary/web_scrap')
            command = 'cp autolibrary/documents/' + unique_key + '/' + pdfname + ' autolibrary/documents_copy/' + unique_key
            os.system(command)
            command = 'cp autolibrary/documents_copy/' + unique_key + '/' + pdfname + ' static/autolibrary/documents'
            os.system(command)

        request.session['myobj'] = shared_obj
        return HttpResponse('get url')
    request.session['myobj'] = shared_obj
    return HttpResponse('fail to get url')

@csrf_exempt
def upload_file(request):
    unique_key = request.session.session_key
    os.system('mkdir -p autolibrary/documents/' + unique_key )
    os.system('mkdir -p autolibrary/documents_copy/' + unique_key )
    if request.method == 'POST':
        if request.method == "POST":
            img = request.FILES.get("file", None)
            # file = request.POST['file']
            # filename = secure_filename(file.filename)
            filename = secure_filename(img.name)
            f1 = os.path.dirname(os.path.realpath(__file__))
            f2 = os.path.dirname(f1)
            # f=(os.path.join(f2,'static/autolibrary/documents'))
            file_path = 'autolibrary/documents/' + unique_key
            f = (os.path.join(f2,file_path))
            with open(os.path.join(f, filename), 'wb') as f:
                for content in img.chunks():
                    f.write(content)

            # global if_customized
            # if_customized = "false"
            # global selected_doc, selected_pdf
            # selected_doc = filename
            # selected_pdf = filename

            shared_obj = request.session['myobj']
            shared_obj["selected_pdf"] = filename
            shared_obj["selected_doc"] = filename
            shared_obj["if_customized"] = "false"
            request.session['myobj'] = shared_obj

            os.system('mkdir -p static/autolibrary/documents')
            os.system('mkdir -p static/autolibrary/web_scrap')
            command = 'cp autolibrary/documents/' + unique_key + '/' + filename + ' autolibrary/documents_copy/' + unique_key
            os.system(command)
            command = 'cp autolibrary/documents_copy/' + unique_key + '/' + filename + ' static/autolibrary/documents'
            os.system(command)



        return HttpResponse('upload file')
    return HttpResponse('fail to upload file')
