from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from lti.ims.tool_provider import DjangoToolProvider
from lti.models import get_or_create_lti_user
from django.contrib.auth import login


from django.conf import settings 


class LTILaunch(View):

    http_method_names = ['post']

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(LTILaunch, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if settings.LTI_DEBUG:
            for k,v in request.POST.items():
                print "{0} : {1}".format(k,v)

        self.setup_tool_provider(request)
        user = get_or_create_lti_user(self.tool_provider)
        login(request, user)
        return self.launch()
        return JsonResponse({'success' : 'OK'})

    def setup_tool_provider(self, request):
        if 'oauth_consumer_key' not in request.POST:
            raise PermissionDenied()  

        consumer_key = settings.LTI_KEY
        secret = settings.LTI_SECRET
        self.tool_provider = DjangoToolProvider(consumer_key, secret, request.POST)
        self.tool_provider.valid_request(request)

    def launch(self):
        if self.tool_provider.is_instructor():
            return self.launch_instructor()
        elif self.tool_provider.is_student():
            return self.launch_student()

    def launch_student(self):
        raise NotImplementedError

    def launch_instructor(self):
        raise NotImplementedError

