from django.conf.urls import patterns, include, url
from recdep.views import DeviceList, DeviceDetail, TextEndpoint

urlpatterns = patterns('',
    url(r'^devices/$', DeviceList.as_view()),
    url(r'^devices/(?P<key>.*)/$', DeviceDetail.as_view()),
    url(r'^text/$', TextEndpoint.as_view()),
)
