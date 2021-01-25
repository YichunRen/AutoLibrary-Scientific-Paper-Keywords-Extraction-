from django.shortcuts import render
from django.http import HttpResponse
import os
from json import dumps 

def index(request):
    data = os.listdir('autolibrary/documents')
    data = dumps(data) 
    return render(request, 'autolibrary/index.html', {"data": data})

def get_file(request, num=1):
    if request.method == 'POST':
        if file_name in request.POST:
            file_name = request.POST['file_name']
            return HttpResponse('success')
    return HttpResponse('FAIL!!!!!')