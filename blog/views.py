from django.shortcuts import render
from .models import BlogArticle
from datetime import datetime


# Create your views here.
def index(request):
    page_name = "blog"
    qset = BlogArticle.objects.filter(published_at__isnull=False, published_at__lte=datetime.now()).order_by("-published_at")[:9]
    latest_articles = qset[:1]
    articles = qset[1:]

    context = {
        "page_name": page_name,
        "latest_articles": latest_articles,
        "articles": articles,
    }

    return render(request, "blog/index.html", context)


def show(request, slug):
    page_name = "blog"
    article = BlogArticle.objects.get(slug=slug)
    context = {"article": article, "page_name": page_name}
    return render(request, "blog/show.html", context)
