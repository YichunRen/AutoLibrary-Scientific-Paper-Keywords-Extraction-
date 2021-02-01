from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('a/', views.get_file, name='get_file'),
    path('result/', views.askforchild, name='result'),
]
