import logging
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .handlers.github import GithubRequestEventHandler
from .handlers.jenkins import JenkinsEventHandler
from .handlers.exceptions import EventNotHandled
from .dispatcher import Dispatcher


class HookView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(HookView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse("OK")

    def post(self, request):
        try:
            dispatcher = Dispatcher(GithubRequestEventHandler, request)
            dispatcher.dispatch()
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
        dispatcher = Dispatcher(JenkinsEventHandler, request)
        dispatcher.dispatch()
        return HttpResponse("OK")
