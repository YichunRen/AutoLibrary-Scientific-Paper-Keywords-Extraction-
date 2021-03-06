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
import time
import datetime
from django.utils import timezone
from django.contrib.sessions.models import Session

def index(request):
    unique_key = str(request.session.session_key)

    # make dir for each user in documents & documents_copy
    command = 'mkdir -p autolibrary/documents/' + unique_key + '/'
    os.system(command)
    command = 'cp autolibrary/documents/* ' + 'autolibrary/documents/' + unique_key
    os.system(command)
    command = 'mkdir -p autolibrary/documents_copy/' + unique_key + '/'
    os.system(command)
    command = 'cp autolibrary/documents_copy/* ' + 'autolibrary/documents_copy/' + unique_key
    os.system(command)

    # make dir in static/autolibrary
    os.system('mkdir -p static/autolibrary/documents')
    os.system('mkdir -p static/autolibrary/web_scrap')

    path = 'autolibrary/documents/' + unique_key + '/'
    data = os.listdir(path)
    data = dumps(data)

    shared_obj = request.session.get('myobj',{})
    shared_obj['selected_doc'] = ''
    shared_obj['selected_pdf'] = ''
    shared_obj['if_customized'] = "true"
    shared_obj['selected_domain'] = ''
    shared_obj['selected_subdomain'] = ''
    shared_obj['selected_keywords'] = ''
    shared_obj['phrases'] = []
    shared_obj['in_queue'] = "false"
    shared_obj['timestamp'] = ''
    request.session['myobj'] = shared_obj
    return render(request, 'autolibrary/index.html', {"data": data})

def result(request):
    unique_key = str(request.session.session_key)

    path = 'autolibrary/documents/' + unique_key + '/'
    data = os.listdir(path)
    domains = json.load(open('../src/domains_full.json'))

    shared_obj = request.session['myobj']
    selected_doc = shared_obj['selected_doc']
    selected_pdf = shared_obj['selected_pdf']

    content = {
        "data": dumps(data),
        "selected_doc": dumps([selected_doc]),
        "selected_pdf": dumps([selected_pdf]),
        "domains": dumps(domains)
    }

    shared_obj['in_queue'] = "false"
    request.session['myobj'] = shared_obj
    return render(request, 'autolibrary/result.html', content)

def customization(request):
    unique_key = str(request.session.session_key)

    path = 'autolibrary/documents/' + unique_key + '/'
    data = os.listdir(path)
    domains = json.load(open('../src/domains_full.json'))

    shared_obj = request.session['myobj']
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
        "unique_key":dumps([unique_key]),
    }

    if if_customized == "false":
        if_customized = "true"
        shared_obj['if_customized'] = if_customized

    shared_obj['in_queue'] = "false"
    request.session['myobj'] = shared_obj
    return render(request, 'autolibrary/customization.html', content)

@csrf_exempt
def get_file(request):
    unique_key = str(request.session.session_key)
    shared_obj = request.session['myobj']
    if request.method == 'POST':
        if "file_name" in request.POST:
            if_customized = "false"
            shared_obj['if_customized'] = if_customized

            # rename document
            file_name = request.POST['file_name']
            pdfname = file_name.replace("'", "")
            pdfname = pdfname.replace(" ", "_")
            # os.system('bash autolibrary/rename.sh')
            shared_obj['selected_pdf'] = pdfname
            shared_obj['selected_doc'] = file_name

            # move selected document to documents_copy and static
            command = 'cp autolibrary/documents/' + unique_key + '/' + pdfname + ' autolibrary/documents_copy/' + unique_key
            os.system(command)
            command = 'cp autolibrary/documents_copy/' + unique_key + '/' + pdfname + ' static/autolibrary/documents'
            os.system(command)

            # rewrite data-params.json
            config = json.load(open('../config/data-params.json'))
            config['pdfname'] = pdfname
            with open('autolibrary/data-params_' + unique_key + '.json', 'w') as fp:
                json.dump(config, fp)
            with open('autolibrary/run_' + unique_key + '.sh', 'w') as rsh:
                # move selected document to data/raw
                rsh.write('''mkdir -p ../data/raw \n''')
                rsh.write('''cp autolibrary/documents_copy/''' + unique_key + '''/''' + pdfname + ''' ../data/raw \n''')
                # move new data-params.json to config
                rsh.write('''cp autolibrary/data-params_''' + unique_key + '''.json  ../config \n''')
                rsh.write('''cd .. \n''')
                rsh.write('''/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py data ''' + unique_key + ''' \n''')
            subprocess.Popen(['bash', 'autolibrary/run_' + unique_key + '.sh'])

            shared_obj['in_queue'] = "false"
            request.session['myobj'] = shared_obj
            return HttpResponse('get file')
    return HttpResponse('fail to get file')

@csrf_exempt
def get_domain1(request):
    unique_key = str(request.session.session_key)
    shared_obj = request.session['myobj']
    if request.method == 'POST':
        if "domain" in request.POST:
            # save selected domain to data/out
            selected_domain = request.POST['domain']
            selected_subdomain = request.POST['subdomain']
            selected_pdf = shared_obj['selected_pdf']
            if selected_domain == '':
                selected_domain = 'ALL'
            if selected_subdomain == '':
                selected_subdomain = 'ALL'

            shared_obj['selected_domain'] = selected_domain
            shared_obj['selected_subdomain'] = selected_subdomain

            # os.system('mkdir -p ../data/out')
            command = 'mkdir -p ../data/out_' + unique_key
            os.system(command)

            # with open('../data/out/selected_domain_' + unique_key + '.txt', 'w') as fp:
            with open('../data/out_' + unique_key + '/selected_domain.txt', 'w') as fp:
                fp.write(selected_subdomain)
            config = {'fos': [selected_domain]}
            # with open('../data/out/fos_' + unique_key + '.json', 'w') as fp:
            with open('../data/out_' + unique_key + '/fos.json', 'w') as fp:
                json.dump(config, fp)

            # # rewrite data-params.json
            # config = json.load(open('../config/data-params.json'))
            # config['pdfname'] = selected_pdf
            # with open('autolibrary/data-params_' + unique_key + '.json', 'w') as fp:
            #     json.dump(config, fp)

            # copy AutoPhrase for each user
            with open('autolibrary/run_' + unique_key + '.sh', 'w') as rsh:
                rsh.write('''cd .. \n''')
                rsh.write('''cp -a /home/yichunren/AutoLibrary/AutoPhrase2/. /home/yichunren/AutoLibrary/AutoPhrase_''' + unique_key + '''/ \n''')
            process = subprocess.Popen(['bash', 'autolibrary/run_' + unique_key + '.sh'])
            process.wait()

            # print to server log
            import sys
            sys.stdout.write("Hello\n")
            # set in_queue and timestamp
            shared_obj['in_queue'] = "true"
            d = datetime.datetime.now(datetime.timezone.utc)
            unix = time.mktime(d.timetuple())
            shared_obj['timestamp'] = unix
            request.session['myobj'] = shared_obj
            request.session.save()
            # calculate wait time
            sessions = Session.objects.filter(expire_date__gte=timezone.now())
            sessions_in_queue = []
            for session in sessions:
                s = session.get_decoded()
                session_obj = s['myobj']
                if 'in_queue' in session_obj:
                    if session_obj['in_queue'] == "true":
                        print('in queue\n')
                        print(session.session_key)
                        if session.session_key != unique_key:
                            print('not myself\n')
                        else:
                            print('myself\n')
                        # update timestamp if duplicate
                        timestamp = session_obj['timestamp']
                        if timestamp in sessions_in_queue:
                            timestamp += 1
                        session_obj['timestamp'] = timestamp
                        session.save()
                        sessions_in_queue.append(timestamp)
            sessions_in_queue.sort()
            print('all sessions in queue\n')
            print(sessions_in_queue)

            # wait if in queue
            shared_obj = request.session['myobj']
            unix = shared_obj['timestamp']
            wait_time = 5 * sessions_in_queue.index(unix)
            # wait_time = 0
            # curr_position = sessions_in_queue.index(unix)
            # if curr_position != 0:
            #     time_gap = sessions_in_queue[curr_position] - sessions_in_queue[curr_position - 1]
            #     if time_gap < 20:
            #         wait_time = 20 - time_gap
            print('selected document\n')
            print(selected_pdf)
            print('wait time\n')
            print(wait_time)
            # time.sleep(wait_time)
            # run autophrase
            with open('autolibrary/run_' + unique_key + '.sh', 'w') as rsh:
                rsh.write('''cd .. \n''')
                rsh.write('''/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py autophrase ''' + unique_key + ''' \n''')
            process = subprocess.Popen(['bash', 'autolibrary/run_' + unique_key + '.sh'])
            process.wait()

            shared_obj['in_queue'] = "false"
            request.session['myobj'] = shared_obj
            return HttpResponse('get domain')
    return HttpResponse('fail to get domain')

@csrf_exempt
def get_domain2(request):
    unique_key = str(request.session.session_key)
    shared_obj = request.session['myobj']
    if request.method == 'POST':
        if "domain" in request.POST:
            # run weight and webscrape
            with open('autolibrary/run_' + unique_key + '.sh', 'w') as rsh:
                rsh.write('''cd .. \n''')
                rsh.write('''/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py weight ''' + unique_key +  ''' \n''')
                rsh.write('''/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py webscrape ''' + unique_key +  ''' \n''')
                rsh.write('''cp data/out_''' + unique_key + '''/scraped_AutoPhrase.json website/static/autolibrary/web_scrap/scraped_AutoPhrase_''' + unique_key + '''.json \n''')
            process = subprocess.Popen(['bash', 'autolibrary/run_' + unique_key + '.sh'])
            process.wait()

            # display phrases with a weighted quality score > 0.5
            data = pd.read_csv('../data/out_' + unique_key + '/weighted_AutoPhrase.csv', index_col = "Unnamed: 0")
            phrases = data[data['score'] > 0.5]['phrase'].to_list()
            if len(phrases) < 5:
                phrases = data['phrase'][:5].to_list()
            shared_obj['phrases'] = phrases

            shared_obj['in_queue'] = "false"
            request.session['myobj'] = shared_obj
            return HttpResponse('get domain')
    return HttpResponse('fail to get domain')

@csrf_exempt
def get_keywords(request):
    unique_key = str(request.session.session_key)
    shared_obj = request.session['myobj']
    if request.method == 'POST':
        if "keywords" in request.POST:
            # save selected keywords to data/out
            selected_keywords = request.POST['keywords']
            shared_obj['selected_keywords'] = selected_keywords
            config = {'keywords': selected_keywords}
            # with open('../data/out/selected_keywords.json', 'w') as fp:
            with open('../data/out_' + unique_key + '/selected_keywords.json', 'w') as fp:
                json.dump(config, fp)

            # display new webscrape result
            with open('autolibrary/run_' + unique_key + '.sh', 'w') as rsh:
                rsh.write('''cd .. \n''')
                rsh.write('''/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py webscrape ''' + unique_key +  ''' \n''')
                rsh.write('''cp data/out_''' + unique_key + '''/scraped_AutoPhrase.json website/static/autolibrary/web_scrap/scraped_AutoPhrase_''' + unique_key + '''.json \n''')
            process = subprocess.Popen(['bash', 'autolibrary/run_' + unique_key + '.sh'])
            process.wait()

            shared_obj['in_queue'] = "false"
            request.session['myobj'] = shared_obj
            return HttpResponse('get keywords')
    return HttpResponse('fail to get keywords')

@csrf_exempt
def get_url(request):
    unique_key = str(request.session.session_key)
    shared_obj = request.session['myobj']
    if request.method == 'POST':
        if "url" in request.POST:
            download_url = request.POST['url']
            filename = download_url.split('/')[-1]
            response = urllib2.urlopen(download_url)

            # save uploaded file
            fp = "autolibrary/documents/" + unique_key + '/' + filename
            file = open(fp, 'wb')
            file.write(response.read())
            file.close()

            if_customized = "false"
            shared_obj['if_customized'] = if_customized
            shared_obj['selected_doc'] = filename
            shared_obj['selected_pdf'] = filename

            # move selected document to documents_copy and static
            command = 'cp autolibrary/documents/' + unique_key + '/' + filename + ' autolibrary/documents_copy/' + unique_key
            os.system(command)
            command = 'cp autolibrary/documents_copy/' + unique_key + '/' + filename + ' static/autolibrary/documents'
            os.system(command)

            # rewrite data-params.json
            config = json.load(open('../config/data-params.json'))
            config['pdfname'] = filename
            with open('autolibrary/data-params_' + unique_key + '.json', 'w') as fp:
                json.dump(config, fp)

            # convert pdf to txt
            with open('autolibrary/run_' + unique_key + '.sh', 'w') as rsh:
                # move selected document to data/raw
                rsh.write('''mkdir -p ../data/raw \n''')
                rsh.write('''cp autolibrary/documents_copy/''' + unique_key + '''/''' + filename + ''' ../data/raw \n''')
                # move new data-params.json to config
                rsh.write('''cp autolibrary/data-params_''' + unique_key + '''.json  ../config \n''')
                rsh.write('''cd .. \n''')
                rsh.write('''/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py data ''' + unique_key + ''' \n''')
            process = subprocess.Popen(['bash', 'autolibrary/run_' + unique_key + '.sh'])
            process.wait()

            shared_obj['in_queue'] = "false"
            request.session['myobj'] = shared_obj
            return HttpResponse('get url')
    return HttpResponse('fail to get url')

@csrf_exempt
def upload_file(request):
    unique_key = str(request.session.session_key)
    shared_obj = request.session['myobj']
    if request.method == 'POST':
        if request.method == "POST":
            img = request.FILES.get("file", None)
            # file = request.POST['file']
            # filename = secure_filename(file.filename)
            filename = secure_filename(img.name)
            f1 = os.path.dirname(os.path.realpath(__file__))
            f2 = os.path.dirname(f1)
            # f = (os.path.join(f2,'static/autolibrary/documents'))
            file_path = 'autolibrary/documents/' + unique_key
            f = (os.path.join(f2, file_path))
            with open(os.path.join(f, filename), 'wb') as f:
                for content in img.chunks():
                    f.write(content)

            shared_obj["selected_pdf"] = filename
            shared_obj["selected_doc"] = filename
            shared_obj["if_customized"] = "false"

            # move selected document to documents_copy and static
            command = 'cp autolibrary/documents/' + unique_key + '/' + filename + ' autolibrary/documents_copy/' + unique_key
            os.system(command)
            command = 'cp autolibrary/documents_copy/' + unique_key + '/' + filename + ' static/autolibrary/documents'
            os.system(command)

            # rewrite data-params.json
            config = json.load(open('../config/data-params.json'))
            config['pdfname'] = filename
            with open('autolibrary/data-params_' + unique_key + '.json', 'w') as fp:
                json.dump(config, fp)

            # convert pdf to txt
            with open('autolibrary/run_' + unique_key + '.sh', 'w') as rsh:
                # move selected document to data/raw
                rsh.write('''mkdir -p ../data/raw \n''')
                rsh.write('''cp autolibrary/documents_copy/''' + unique_key + '''/''' + filename + ''' ../data/raw \n''')
                # move new data-params.json to config
                rsh.write('''cp autolibrary/data-params_''' + unique_key + '''.json  ../config \n''')
                rsh.write('''cd .. \n''')
                rsh.write('''/home/yichunren/AutoLibrary/myvenv/bin/python /home/yichunren/AutoLibrary/run.py data ''' + unique_key + ''' \n''')
            process = subprocess.Popen(['bash', 'autolibrary/run_' + unique_key + '.sh'])
            process.wait()

            shared_obj['in_queue'] = "false"
            request.session['myobj'] = shared_obj
            return HttpResponse('upload file')
    return HttpResponse('fail to upload file')
