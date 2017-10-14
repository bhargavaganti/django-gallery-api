from django.conf.urls import url
from rest_framework.compat import include
from src.images.api.views import GetImagesAPI
from src.images.api.views import GetAllImages
from .views import CreateGetAlbumsAPI, AlbumDetailAPIView

urlpatterns = [
    # url(r'(?P<album_id>\d+)/images/(?P<image_id>\d+)/?$', GetDetailImage.as_view(), name='album-images'),
    url(r'(?P<album_id>\d+)/images/?', include("src.images.api.urls", namespace='album-images')),
    url(r'(?P<album_id>\d+)/?$', AlbumDetailAPIView.as_view(), name='detail'),  # TODO: обриши имена
    url(r'$', CreateGetAlbumsAPI.as_view(), name='list')
]


