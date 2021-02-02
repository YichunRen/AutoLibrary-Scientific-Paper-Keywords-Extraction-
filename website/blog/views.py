from django.shortcuts import render
from django.http import HttpResponse
import os
import json
from json import dumps 
from django.views.decorators.csrf import csrf_exempt

def index(request):
    data = os.listdir('autolibrary/documents')
    data = dumps(data) 
    return render(request, 'blog/index.html', {"data": data})

# @csrf_exempt
# def get_file(request):
#     if request.method == 'POST':
#         if "file_name" in request.POST:
#             # rename document
#             file_name = request.POST['file_name']
#             pdfname = file_name.replace("'", "")
#             pdfname = pdfname.replace(" ", "_")
#             os.system('bash autolibrary/rename.sh')
#             # rewrite data-params.json
#             config = {
#                 "indir": "data/raw",
#                 "outdir": "data/temp",
#                 "pdfname": pdfname
#             }
#             with open('autolibrary/data-params.json', 'w') as fp:
#                 json.dump(config, fp)
#             with open('autolibrary/run.sh', 'w') as rsh:
#                 # move document to data/raw
#                 rsh.write('''mkdir -p ../data/raw \n''')
#                 rsh.write('''cp autolibrary/documents_copy/''')
#                 rsh.write(pdfname)
#                 rsh.write(''' ../data/raw \n''')
#                 # move new data-params.json to config
#                 rsh.write('''cp autolibrary/data-params.json  ../config \n''')
#                 rsh.write('''cd .. \n''')
#                 rsh.write('''python run.py data \n''')
#                 #rsh.write('''python run.py autophrase \n''')
#                 #rsh.write('''python run.py weight \n''')
#             os.system('bash autolibrary/run.sh')
#             return HttpResponse('success')
#     return HttpResponse('FAIL!!!!!')
