from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .parsers import GithubRequestEventParser


class HookView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(HookView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse('GET')

    def post(self, request):
        event = GithubRequestEventParser()
        event.parse(request)
        print request.body
        return HttpResponse("OK")
