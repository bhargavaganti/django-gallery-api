from django.conf.urls import url

from src.albums.api.views import GetAlbumsAPI, AlbumDetailAPIView
from .views import GetProfilesAPI, CreateProfileAPI,ProfileDetailAPIView

urlpatterns = [

    url(r'(?P<pk>\d+)/albums/(?P<album_id>\d+)/?$', AlbumDetailAPIView.as_view(), name='profile-album'),
    url(r'(?P<pk>\d+)/albums/?$', GetAlbumsAPI.as_view(), name='albums'),
    url(r'(?P<pk>\d+)/?$', ProfileDetailAPIView.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateProfileAPI.as_view(), name='create'),
    url(r'$', GetProfilesAPI.as_view(), name='list')

]

