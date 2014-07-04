from django.conf.urls import patterns, include, url
from django.contrib import admin
import recdep.urls

urlpatterns = patterns('',
    ('^v1/', include('recdep.urls')),
)
