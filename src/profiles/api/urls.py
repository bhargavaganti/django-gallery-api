from django.conf.urls import url

from src.albums.api.views import GetAlbumsAPI, AlbumDetailAPIView

from .views import GetProfilesAPI, CreateProfileAPI,ProfileDetailAPIView
from src.images.api.views import GetImagesAPI
from src.images.api.views import ImageDetailAPIView
from src.tags.api.views   import GetTagsAPI
from src.tags.api.views   import TagDetailAPIView
from src.likes.api.views  import GetLikesAPI
from src.likes.api.views  import LikeDetailAPIView
from src.likes.api.views  import CreateLikeAPI

urlpatterns = [

    url(r'(?P<pk>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/likes/(?P<like_id>\d+)/?$', LikeDetailAPIView.as_view(),name='profile-album-image-like'),
    url(r'(?P<pk>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/likes/create/?$', CreateLikeAPI.as_view(),name='profile-album-image-likes-create'),
    url(r'(?P<pk>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/likes/?$', GetLikesAPI.as_view(),name='profile-album-image-likes'),

    url(r'(?P<pk>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/tags/(?P<tag_id>\d+)/?$', TagDetailAPIView.as_view(), name='profile-album-image-tag'),
    url(r'(?P<pk>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/tags/?$', GetTagsAPI.as_view(), name='profile-album-image-tags'),

    url(r'(?P<pk>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/?$', ImageDetailAPIView.as_view(), name='profile-album-image'),
    url(r'(?P<pk>\d+)/albums/(?P<album_id>\d+)/images/?$', GetImagesAPI.as_view(), name='profile-album-images'),

    url(r'(?P<pk>\d+)/albums/(?P<album_id>\d+)/?$', AlbumDetailAPIView.as_view(), name='profile-album'),
    url(r'(?P<pk>\d+)/albums/?$', GetAlbumsAPI.as_view(), name='albums'),

    url(r'(?P<pk>\d+)/?$', ProfileDetailAPIView.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateProfileAPI.as_view(), name='create'),
    url(r'$', GetProfilesAPI.as_view(), name='list')

]

