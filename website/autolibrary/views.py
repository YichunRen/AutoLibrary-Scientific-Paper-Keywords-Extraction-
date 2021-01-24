from django.shortcuts import render
from django.http import HttpResponse
import os


def index(request):
    return HttpResponse("Hello, world. You're at the AutoLibrary page.")
    #return render(request, os.path.dirname(os.path.realpath(__file__)) + '/code/index.html')
