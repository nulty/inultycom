from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def home(request):
    page_name = "home"
    template = loader.get_template("main/home.html")
    context = {
        "page_name": page_name,
    }
    return HttpResponse(template.render(context, request))


def work(request):
    page_name = "work"
    template = loader.get_template("main/work.html")
    context = {"page_name": page_name, "years": 9}
    return HttpResponse(template.render(context, request))
