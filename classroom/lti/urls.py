from django.conf.urls import patterns, include, url
from views import LTILaunch, lti_view

urlpatterns = patterns('',
    url(r'^launch/$', LTILaunch.as_view(),name="lti_launch"),
    url(r'^view/$', lti_view, name="lti_view")

)

