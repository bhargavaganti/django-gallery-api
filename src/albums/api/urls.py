from django.conf.urls import url
from .views import GetAlbumsAPI, CreateAlbumAPI, AlbumDetailAPIView

urlpatterns = [
    url(r'(?P<pk>\d+)/?$', AlbumDetailAPIView.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateAlbumAPI.as_view(), name='create'),
    url(r'$', GetAlbumsAPI.as_view(), name='list')
]


