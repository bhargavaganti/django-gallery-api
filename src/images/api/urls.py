from django.conf.urls import url
from django.contrib import admin

from .views import GetImagesAPI, GetImageAPI, CreateImageAPI, UpdateImageAPI, DeleteImageAPI

urlpatterns = [
    url(r'(?P<pk>\d+)/delete/?$', DeleteImageAPI.as_view(), name='delete'),
    url(r'(?P<pk>\d+)/edit/?$', UpdateImageAPI.as_view(), name='update'),
    url(r'(?P<pk>\d+)/?$', GetImageAPI.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateImageAPI.as_view(), name='create'),
    url(r'$', GetImagesAPI.as_view(), name='list')

]


