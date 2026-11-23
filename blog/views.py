from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone

from .models import BlogArticle


def index(request):
    page_name = "blog"
    qset = BlogArticle.objects.published().order_by("-published_at")[:9]
    latest_articles = qset[:1]
    articles = qset[1:]

    context = {
        "page_name": page_name,
        "latest_articles": latest_articles,
        "articles": articles,
    }

    return render(request, "blog/index.html", context)


def show(request, slug):
    """Published articles are public; drafts and scheduled ones are staff-only previews."""
    articles = BlogArticle.objects.filter(slug=slug)
    if not request.user.is_staff:
        articles = articles.published()
    article = articles.order_by("-id").first()
    if article is None:
        raise Http404("No such article")

    context = {"article": article, "page_name": "blog", "preview": not article.is_published}
    return render(request, "blog/show.html", context)


def preview_file(request, path):
    """DEBUG only: render a Markdown file from the project as an article.

    /blog/preview/post_1_revised.md renders <project>/post_1_revised.md through the
    article template without touching the database. A leading `# Heading` becomes
    the title.
    """
    if not settings.DEBUG:
        raise Http404

    base = Path(settings.BASE_DIR).resolve()
    file = (base / path).resolve()
    if file.suffix != ".md" or not file.is_relative_to(base) or not file.is_file():
        raise Http404("No such Markdown file")

    body = file.read_text()
    title = file.stem.replace("_", " ").replace("-", " ").capitalize()
    first, _, rest = body.lstrip().partition("\n")
    if first.startswith("# "):
        title, body = first[2:].strip(), rest

    article = BlogArticle(
        title=title,
        sub_title=f"Preview of {path}",
        body=body,
        slug=file.stem,
        created_at=timezone.now(),
    )
    context = {"article": article, "page_name": "blog", "preview": True, "preview_file": path}
    return render(request, "blog/show.html", context)
