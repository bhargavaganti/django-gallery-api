from django.conf.urls import url, include
from django.contrib import admin

from src.tags.api.views import TagDetailAPIView

from src.tags.api.views import GetTagsAPI
from .views import GetImagesAPI, CreateImageAPI, ImageDetailAPIView, GetAllImages, GetImage, GetTopImages, \
    GetOwnerImages

urlpatterns = [
    # да ли направити све ове руте? лајкови, коментари?
    # url(r'(?P<image_id>\d+)/tags/(?P<tag_id>\d+)/?$', TagDetailAPIView.as_view(), name='image-tag'),
    # url(r'(?P<image_id>\d+)/tags/?$', GetTagsAPI.as_view(), name='image-tags'),
    url(r'profile/(?P<profile_id>\d+)/?$', GetOwnerImages.as_view(), name='profile'),
    url(r'(?P<image_id>\d+)/comments/?', include("src.comments.api.urls", namespace='image-comments')),
    url(r'(?P<image_id>\d+)/likes/?', include("src.likes.api.urls", namespace='image-likes')),
    url(r'(?P<image_id>\d+)/tags/?', include("src.tags.api.urls", namespace='image-tags')),
    url(r'(?P<image_id>\d+)/?$', GetImage.as_view(), name='detail'),
    # url(r'create/?$', CreateImageAPI.as_view(), name='create'),
    url(r'top/?$', GetTopImages.as_view(), name='top'),
    url(r'$', GetAllImages.as_view(), name='list')
]


