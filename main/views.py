from django.core.cache import cache
from django.http import HttpResponse
from django.template import loader
from main.lib.github.events import GitHubEvents
import requests
import logging

logger = logging.getLogger(__name__)

GITHUB_EVENTS_URL = "https://api.github.com/users/nulty/events/public?per_page=6"
# Unauthenticated GitHub API is limited to 60 requests/hour per IP.
GITHUB_CACHE_SECONDS = 600


def home(request):
    page_name = "home"
    template = loader.get_template("main/home.html")

    github_events = GitHubEvents(github_activity()).events

    context = {"page_name": page_name, "years": 9, "github_events": github_events}
    return HttpResponse(template.render(context, request))


def github_activity():
    cached = cache.get("github_activity")
    if cached is not None:
        return cached

    try:
        response = requests.get(GITHUB_EVENTS_URL, timeout=3)
        response.raise_for_status()
        events = response.json()
    except (requests.RequestException, ValueError) as e:
        logger.warning("GitHub activity fetch failed: %s", e)
        # Back off briefly rather than hammering GitHub on every request.
        cache.set("github_activity", [], 60)
        return []

    cache.set("github_activity", events, GITHUB_CACHE_SECONDS)
    return events
