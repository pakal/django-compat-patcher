"""
test_project URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse

urlpatterns = [
    url(r'^homepage/$', lambda r: HttpResponse("HELLO"), name="homepage"),
    url(r'^admin/', admin.site.urls, name="admin"),
]
