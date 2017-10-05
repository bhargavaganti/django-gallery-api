from django.conf.urls import url

from .views import GetProfilesAPI, CreateProfileAPI,ProfileDetailAPIView
from src.albums.api.views import GetAlbumsAPI, AlbumDetailAPIView, CreateAlbumAPI
from src.images.api.views import GetImagesAPI, ImageDetailAPIView, CreateImageAPI
from src.tags.api.views   import GetTagsAPI, TagDetailAPIView, CreateTagAPI
from src.likes.api.views  import GetLikesAPI, LikeDetailAPIView, CreateLikeAPI
from src.comments.api.views import GetCommentsAPI, CreateCommentAPI, CommentDetailAPIView

urlpatterns = [

    url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/comments/(?P<comment_id>\d+)/?$',CommentDetailAPIView.as_view(), name='profile-album-image-comment'),
    url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/comments/create/?$', CreateCommentAPI.as_view(),name='profile-album-image-comments-create'),
    url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/comments/?$', GetCommentsAPI.as_view(),name='profile-album-image-comments'),

    url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/likes/(?P<like_id>\d+)/?$', LikeDetailAPIView.as_view(),name='profile-album-image-like'),
    url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/likes/create/?$', CreateLikeAPI.as_view(),name='profile-album-image-likes-create'),
    url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/likes/?$', GetLikesAPI.as_view(),name='profile-album-image-likes'),

    url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/tags/(?P<tag_id>\d+)/?$', TagDetailAPIView.as_view(), name='profile-album-image-tag'),
    url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/tags/create/?$', CreateTagAPI.as_view(), name='profile-album-image-tags-create'),
    url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/tags/?$', GetTagsAPI.as_view(), name='profile-album-image-tags'),

    url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/?$', ImageDetailAPIView.as_view(), name='profile-album-image'),
    url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/create/?$', CreateImageAPI.as_view(), name='profile-album-images-create'),
    url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/images/?$', GetImagesAPI.as_view(), name='profile-album-images'),

    url(r'(?P<profile_id>\d+)/albums/(?P<album_id>\d+)/?$', AlbumDetailAPIView.as_view(), name='profile-album'),
    url(r'(?P<profile_id>\d+)/albums/create/?$', CreateAlbumAPI.as_view(), name='albums-create'),
    url(r'(?P<profile_id>\d+)/albums/?$', GetAlbumsAPI.as_view(), name='albums'),

    url(r'(?P<profile_id>\d+)/?$', ProfileDetailAPIView.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateProfileAPI.as_view(), name='create'),
    url(r'$', GetProfilesAPI.as_view(), name='list')

]

