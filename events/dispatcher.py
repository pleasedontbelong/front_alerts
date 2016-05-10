from django.conf import settings


class Dispatcher(object):
    def __init__(self):
        config = settings.MESSAGES_ROUTING.copy()
        default_config = config.pop('default')
        self.routes = []
        for route_name, route_config in config.iteritems():
            self.routes.append(
                EventRoute(default_config, route_name, route_config)
            )
        self.sent = False

    def dispatch(self, event):
        for route in self.routes:
            if route.should_send(event):
                self.sent = True
                route.send(event)


class EventRoute(object):
    def __init__(self, default_config, route_name, route_config):
        self.config = default_config.copy()
        self.config.update(route_config)
        self.route_name = route_name

    def should_send(self, event):
        return event.should_send(trigger_labels=self.config.get('github_labels'))

    def send(self, event):
        event.send(self.config.get("slack_channels"), self.config.get("review_request_label"))
