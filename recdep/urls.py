from django.conf.urls import patterns, include, url
from recdep.views import DeviceList

urlpatterns = patterns('',
    url(r'^devices/$', DeviceList.as_view()),
    url(r'^device/(?P<fk>.*)/$', DeviceList.as_view()),
)
