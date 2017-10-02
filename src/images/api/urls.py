from django.conf.urls import url, include
from django.contrib import admin

from src.tags.api.views import TagDetailAPIView

from src.tags.api.views import GetTagsAPI
from .views import GetImagesAPI, CreateImageAPI, ImageDetailAPIView

urlpatterns = [
    # url(r'(?P<image>\d+)/tags/(?P<tag>\d+)/?$', GetTagsAPI.as_view(), name='image-tag'),  # TODO: обриши имена
    url(r'(?P<pk>\d+)/tags/?$', GetTagsAPI.as_view(), name='image-tags'),  # TODO: обриши имена
    url(r'(?P<pk>\d+)/?$', ImageDetailAPIView.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateImageAPI.as_view(), name='create'),
    url(r'$', GetImagesAPI.as_view(), name='list')
]


