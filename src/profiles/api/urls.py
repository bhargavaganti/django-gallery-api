from django.conf.urls import url

from .views import GetProfilesAPI, CreateProfileAPI,ProfileDetailAPIView
from src.albums.api.views import GetAlbumsAPI, AlbumDetailAPIView
from src.images.api.views import GetImagesAPI, ImageDetailAPIView
from src.tags.api.views   import GetTagsAPI, TagDetailAPIView
from src.likes.api.views  import GetLikesAPI, LikeDetailAPIView, CreateLikeAPI
from src.comments.api.views import GetCommentsAPI, CreateCommentAPI, CommentDetailAPIView

urlpatterns = [

    url(r'(?P<pk>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/comments/(?P<comment_id>\d+)/?$',CommentDetailAPIView.as_view(), name='profile-album-image-comment'),
    url(r'(?P<pk>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/comments/create/?$', CreateCommentAPI.as_view(),name='profile-album-image-comments-create'),
    url(r'(?P<pk>\d+)/albums/(?P<album_id>\d+)/images/(?P<image_id>\d+)/comments/?$', GetCommentsAPI.as_view(),name='profile-album-image-comments'),

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

