from django.conf.urls import url, include

from . import views
from src.albums.api.views import *

urlpatterns = [

        # Прво сам писао овако, крајњу тачку по крајњу тачку, без потребе. Али Ђанго је зато и модуларан,
        # да не би било овога.Потребно је само укључити пакет рута, и написати их тако да буду модуларне и прилагодљиве.

    # url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/comments/(?P<comment_id>\d+)/?$', CommentDetailAPIView.as_view(), name='profile-album-image-comment'),
    # url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/comments/?$', CreateGetCommentsAPI.as_view(), name='profile-album-image-comments'),
    # url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/likes/(?P<like_id>\d+)/?$', LikeDetailAPIView.as_view(), name='profile-album-image-like'),
    # url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/likes/create/?$', CreateLikeAPI.as_view(), name='profile-album-image-likes-create'),
    # url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/likes/?$', GetLikesAPI.as_view(),name='profile-album-image-likes'),
    # url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/tags/(?P<tag_id>\d+)/?$',TagDetailAPIView.as_view(), name='profile-album-image-tag'),
    # url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/tags/create/?$', CreateTagAPI.as_view(),name='profile-album-image-tags-create'),
    # url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/tags/?$', GetTagsAPI.as_view(),name='profile-album-image-tags'),
    # url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/?$', ImageDetailAPIView.as_view(),name='profile-album-image'),
    # url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/?',include("src.images.api.urls", name='profile-album-images')),
    # url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/?$', AlbumDetailAPIView.as_view(), name='profile-album'),

    url(r'(?P<profile_id>\d+)/albums/?', include("src.albums.api.urls", namespace='albums')),
    url(r'(?P<profile_id>\d+)/?$', views.ProfileDetailAPIView.as_view(), name='detail'),
    url(r'$', views.CreateGetProfilesAPI.as_view(), name='list-create')

]
