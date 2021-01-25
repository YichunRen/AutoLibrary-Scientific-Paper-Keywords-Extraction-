from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/a', views.get_file, name='get_file'),
    #path('page<int:num>', views.get_file),
    #url('/autolibrary', views.get_file),
]