from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.askforchild, name='result'),
    path('customization/', views.customization, name='customization'),
    path('a/', views.get_file, name='get_file'),
    path('b/', views.get_domain, name='get_domain'),
    path('c/', views.get_customization, name='get_customization'),
]
