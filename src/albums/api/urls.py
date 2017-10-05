from django.conf.urls import url
from src.images.api.views import GetImagesAPI
from src.images.api.views import GetAllImages
from .views import GetAlbumsAPI, CreateAlbumAPI, AlbumDetailAPIView

urlpatterns = [
    # TODO: имплементирати овде остатак?
    url(r'(?P<album_id>\d+)/images/?$', GetAllImages.as_view(), name='album-images'),  # TODO: обриши имена
    url(r'(?P<album_id>\d+)/?$', AlbumDetailAPIView.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateAlbumAPI.as_view(), name='create'),
    url(r'$', GetAlbumsAPI.as_view(), name='list')
]


