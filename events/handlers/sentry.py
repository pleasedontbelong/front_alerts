import json
from .core import EventHandler
from events.constants import SLACK_COLORS


class SentryErrorEvent(EventHandler):

    def __init__(self, *args, **kwargs):
        self.payload = None
        super(SentryErrorEvent, self).__init__(*args, **kwargs)

    def get_attachments(self, payload, route_config):
        plain = "Sentry Error on {}".format(payload["project_name"])
        return [{
            "author_name": plain,
            "author_link": payload["url"],
            "fallback": plain,
            "color": SLACK_COLORS.DANGER,
            "title": payload["culprit"],
            "text": ":scream: " + payload["message"],
        }]

    def should_send(self, payload, route_config):
        project_name = payload["project"]
        trigger_project_names = route_config.get("sentry_projects")
        return project_name in trigger_project_names

    def get_event_id(self, payload):
        return payload['id']

    def get_event_name(self, payload):
        return u"sentry_error"


class SentryEventHandler(object):

    def __init__(self, request):
        self.request = request
        self.payload = json.loads(self.request.body)
        self.event_class = SentryErrorEvent()

    def send(self, route_config):
        self.event_class.send(self.payload, route_config)

    def should_send(self, route_config):
        return self.event_class.should_send(self.payload, route_config)

    @property
    def event_id(self):
        return self.event_class.get_event_id(self.payload)

    @property
    def event_name(self):
        return self.event_class.get_event_name(self.payload)
