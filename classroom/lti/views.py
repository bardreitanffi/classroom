from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

class LTILaunch(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        return JsonResponse({'success' : 'OK'})
