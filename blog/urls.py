from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('preview/<path:path>', views.preview_file, name='preview_file'),
    path('<str:slug>', views.show, name='show'),
]
