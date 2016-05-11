from django.conf import settings
from .models import Event


class Dispatcher(object):

    def __init__(self, event_handler_cls, request):
        self.sent = False
        # initialize all the event routes
        config = settings.MESSAGES_ROUTING.copy()
        default_config = config.pop('default')
        self.routes = []
        for route_name, route_config in config.iteritems():
            self.routes.append(
                EventRoute(default_config, route_name, route_config)
            )

        # initialize the event handler
        self.event_handler = event_handler_cls(request)

    def dispatch(self):
        for route in self.routes:
            if route.should_send(self.event_handler):
                route.send(self.event_handler)

                Event.objects.create(
                    event_data=self.event_handler.payload,
                    event_name=self.event_handler.event_name,
                    event_id=self.event_handler.event_id
                )


class EventRoute(object):
    def __init__(self, default_config, route_name, route_config):
        self.config = default_config.copy()
        self.config.update(route_config)
        self.route_name = route_name

    def should_send(self, event):
        return event.should_send(route_config=self.config)

    def send(self, event):
        event.send(self.config)
