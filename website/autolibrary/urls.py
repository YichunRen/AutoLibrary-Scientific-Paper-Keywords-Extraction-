from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('customization/', views.customization, name='customization'),
    path('a/', views.get_file, name='get_file'),
    path('b/', views.get_domain1, name='get_domain1'),
    path('c/', views.get_domain2, name='get_domain2'),
    path('d/', views.get_keywords, name='get_keywords'),
    path('e/', views.get_url, name='get_url'),
    path('f/', views.upload_file, name='upload_file'),
]
