from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from lti.ims.tool_provider import DjangoToolProvider

from django.conf import settings 


class LTILaunch(View):

    http_method_names = ['post', 'get']

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(LTILaunch, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if settings.LTI_DEBUG:
            for k,v in request.POST.items():
                print "{0} : {1}".format(k,v)

        self.setup_tool_provider(request)
        

        return JsonResponse({'success' : 'OK'})

    def get(self, request, *args, **kwargs):
        return JsonResponse({'success' : 'BAD'})

    def setup_tool_provider(self, request):
        if 'oauth_consumer_key' not in request.POST:
            raise PermissionDenied()  

        consumer_key = settings.LTI_KEY
        secret = settings.LTI_SECRET
        self.tool_provider = DjangoToolProvider(consumer_key, secret, request.POST)
        self.tool_provider.valid_request(request)




