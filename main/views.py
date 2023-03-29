from django.http import HttpResponse
from django.template import loader
from django.views.decorators.cache import cache_page
from main.lib.github.events import GitHubEvents
import requests

# import logging
# logger = logging.getLogger(__name__)


@cache_page(15)
def home(request):
    page_name = "home"
    template = loader.get_template("main/home.html")

    # Leave this here for testing
    # github_activity = json.loads(open("main/github.json", "r").read())
    github_events = GitHubEvents(github_activity()).events

    context = {"page_name": page_name, "github_events": github_events}
    return HttpResponse(template.render(context, request))


def github_activity():
    response = requests.get(
        "https://api.github.com/users/nulty/events/public?per_page=6"
    )
    if response.ok:
        return response.json()
    else:
        return []


def work(request):
    page_name = "work"
    template = loader.get_template("main/work.html")
    context = {"page_name": page_name, "years": 9}
    return HttpResponse(template.render(context, request))
