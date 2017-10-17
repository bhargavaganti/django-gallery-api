from django.conf.urls import url
from rest_framework.compat import include
from .views import CreateGetAlbumsAPI, AlbumDetailAPIView

urlpatterns = [
    url(r'(?P<album_id>\d+)/images/?', include("src.images.api.urls", namespace='album-images')),
    url(r'(?P<album_id>\d+)/?$', AlbumDetailAPIView.as_view(), name='detail'),
    url(r'$', CreateGetAlbumsAPI.as_view(), name='list')
]


