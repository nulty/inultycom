from django.utils.dateparse import parse_datetime
import logging
logger = logging.getLogger(__name__)
import re

def web_url(url):
    url = re.sub("api.", "www.", url)
    url = re.sub("repos/", "", url)
    return url 

class GitHubEvents:
    def __init__(self, data):
        self.events = []
        for event in data:
            match event['type']:
                case 'PushEvent':
                    self.events.append(PushEvent(event))
                case 'CreateEvent':
                    self.events.append(CreateEvent(event))

class GitHubEvent:
    def __init__(self, event):
        self.data = event
        self.type = self.data["type"]
        self.actor = Actor(event["actor"])
        if self.data.get("repo"):
            self.repo = Repository(event.get("repo"))
        # if self.data.get("payload"):
        self.payload = Payload(event.get("payload"))
        self.public = self.data["public"]
        self.created_at = parse_datetime(self.data["created_at"])


class Commit:
    def __init__(self, data):
        self.sha = data.get("sha")
        self.url = web_url(data.get("url"))
        self.author = data.get("author")
        self.message = data.get("message")


class Payload:
    def __init__(self, data):
        self.data = data
        self.commits = []
        if data.get("commits"):
            self.commits = [Commit(item) for item in data.get('commits')]
        self.ref = data.get("ref")
        self.ref_type = data.get("ref_type")
        self.description = data.get("description")
        self.size = data.get("size")


class Actor:
    def __init__(self, data):
        self.id = data.get("id")
        self.url = web_url(data.get("url"))
        self.display_login = data.get("display_login")


class Repository:
    def __init__(self, data):
        self.id = data.get("id")
        self.url = web_url(data.get("url"))
        self.name = data.get("name")


class PushEvent(GitHubEvent):
    def __init__(self, event):
        super().__init__(event)
        self.template = "push"


class CreateEvent(GitHubEvent):
    def __init__(self, event):
        super().__init__(event)
        self.template = "create"
