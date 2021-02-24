from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('customization/', views.customization, name='customization'),
    path('a/', views.get_file, name='get_file'),
    path('b/', views.get_domain, name='get_domain'),
    path('c/', views.get_keywords, name='get_keywords'),
    path('d/', views.get_url, name='get_url'),
    path('e/', views.upload_file, name='upload_file'),
    # path('f/', views.upload, name='upload'),
]
