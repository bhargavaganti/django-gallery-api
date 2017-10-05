from django.conf.urls import url, include
from django.contrib import admin

from src.tags.api.views import TagDetailAPIView

from src.tags.api.views import GetTagsAPI
from .views import GetImagesAPI, CreateImageAPI, ImageDetailAPIView, GetAllImages, GetImage

urlpatterns = [
    # да ли направити све ове руте? лајкови, коментари?
    url(r'(?P<image_id>\d+)/tags/(?P<tag_id>\d+)/?$', TagDetailAPIView.as_view(), name='image-tag'),  # TODO: обриши имена
    url(r'(?P<image_id>\d+)/tags/?$', GetTagsAPI.as_view(), name='image-tags'),  # TODO: обриши имена
    url(r'(?P<image_id>\d+)/?$', GetImage.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateImageAPI.as_view(), name='create'),
    url(r'$', GetAllImages.as_view(), name='list')
]


