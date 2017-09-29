from django.conf.urls import url
from django.contrib import admin

from .views import GetTagsAPI, CreateTagAPI, GetTagAPI, DeleteTagAPI

urlpatterns = [
    url(r'(?P<pk>\d+)/delete/?$', DeleteTagAPI.as_view(), name='delete'),
    # url(r'(?P<pk>\d+)/edit/?$', UpdateTagAPI.as_view(), name='update'),
    url(r'(?P<pk>\d+)/?$', GetTagAPI.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateTagAPI.as_view(), name='create'),
    url(r'$', GetTagsAPI.as_view(), name='list')

]


