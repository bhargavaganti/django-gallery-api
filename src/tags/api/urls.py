from django.conf.urls import url
from django.contrib import admin

from .views import GetTagsAPI, CreateTagAPI, TagDetailAPIView

urlpatterns = [
    url(r'(?P<pk>\d+)/images/?$', TagDetailAPIView.as_view(), name='detail'),  # TODO: обриши имена
    url(r'(?P<pk>\d+)/?$', TagDetailAPIView.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateTagAPI.as_view(), name='create'),
    url(r'$', GetTagsAPI.as_view(), name='list')

]


