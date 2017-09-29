from django.conf.urls import url
from django.contrib import admin

from .views import GetAlbumsAPI, CreateAlbumAPI, GetAlbumAPI, UpdateAlbumAPI, DeleteAlbumAPI

urlpatterns = [
    url(r'(?P<pk>\d+)/delete/?$', DeleteAlbumAPI.as_view(), name='delete'),
    url(r'(?P<pk>\d+)/edit/?$', UpdateAlbumAPI.as_view(), name='update'),
    url(r'(?P<pk>\d+)/?$', GetAlbumAPI.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateAlbumAPI.as_view(), name='create'),
    url(r'$', GetAlbumsAPI.as_view(), name='list')

]


