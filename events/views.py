import logging
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .handlers.github import GithubRequestEventHandler
from .handlers.jenkins import JenkinsEventHandler
from .handlers.exceptions import EventNotHandled
from .models import Event
from .dispatcher import Dispatcher


class HookView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(HookView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse("OK")

    def post(self, request):
        try:
            event = GithubRequestEventHandler(request)
            dispatcher = Dispatcher()
            dispatcher.dispatch(event)
            if dispatcher.sent:
                Event.objects.create(
                    event_data=event.payload,
                    event_name=event.event_name,
                    event_id=event.event_id
                )
        except EventNotHandled, e:
            logging.warning(str(e))
        return HttpResponse("OK")


class JenkinsPRView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(JenkinsPRView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse("OK")

    def post(self, request):
        event = JenkinsEventHandler(request)
        dispatcher = Dispatcher()
        dispatcher.dispatch(event)
        if dispatcher.sent:
            Event.objects.create(
                event_data=event.payload,
                event_name=event.event_name,
                event_id=event.event_id
            )
        return HttpResponse("OK")
