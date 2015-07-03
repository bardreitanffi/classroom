from django.conf.urls import patterns, include, url
from views import LTILaunch

from views import LTILaunch

urlpatterns = patterns('',
    url(r'^launch/$', LTILaunch.as_view(),name="lti_launch")

)

