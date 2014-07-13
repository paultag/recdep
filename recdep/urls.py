from django.conf.urls import patterns, include, url
from recdep.views import (DeviceList, DeviceDetail,
                          PlaceList, PlaceDetail,
                          APList, APDetail,
                          TextEndpoint)

urlpatterns = patterns('',
    url(r'^devices/$', DeviceList.as_view()),
    url(r'^devices/(?P<key>.*)/$', DeviceDetail.as_view()),

    url(r'^places/$', PlaceList.as_view()),
    url(r'^places/(?P<key>.*)/$', PlaceDetail.as_view()),

    url(r'^aps/$', APList.as_view()),
    url(r'^ap/(?P<key>.*)/$', APDetail.as_view()),

    url(r'^text/$', TextEndpoint.as_view()),
)
