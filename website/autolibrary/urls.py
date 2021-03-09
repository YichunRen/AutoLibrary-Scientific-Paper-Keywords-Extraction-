from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('customization/', views.customization, name='customization'),
    path('a/', views.get_file, name='get_file'),
    path('b/', views.get_domain1, name='get_domain1'),
    path('bb/', views.close_domain, name='close_domain'),
    path('c/', views.get_queue, name='get_queue'),
    path('d/', views.get_domain2, name='get_domain2'),
    path('e/', views.get_domain3, name='get_domain3'),
    path('f/', views.get_keywords, name='get_keywords'),
    path('g/', views.get_url, name='get_url'),
    path('h/', views.upload_file, name='upload_file'),
]
