from django.conf.urls import url
from django.contrib import admin

from .views import GetTagsAPI, CreateTagAPI, TagDetailAPIView, TagImagesAPI

urlpatterns = [
    url(r'(?P<tag_id>\d+)/images/?$', TagImagesAPI.as_view(), name='tag-images'),  # TODO: обриши имена
    url(r'(?P<tag_id>\d+)/?$', TagDetailAPIView.as_view(), name='detail'),  # TODO: обриши имена
    url(r'create/?$', CreateTagAPI.as_view(), name='create'),
    url(r'$', GetTagsAPI.as_view(), name='list')

]


