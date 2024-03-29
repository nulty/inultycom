from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:slug>', views.show, name='show'),
    path('<int:id>', views.show, name='show'),
]
