from django.conf.urls import url

from src.images.api.views import GetImagesAPI
from .views import GetAlbumsAPI, CreateAlbumAPI, AlbumDetailAPIView

urlpatterns = [
    url(r'(?P<pk>\d+)/images/?$', GetImagesAPI.as_view(), name='album-images'),  # TODO: обриши имена
    url(r'(?P<pk>\d+)/?$', AlbumDetailAPIView.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateAlbumAPI.as_view(), name='create'),
    url(r'$', GetAlbumsAPI.as_view(), name='list')
]


