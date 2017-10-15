from django.conf.urls import url, include
from django.contrib import admin

from .views import TagDetailAPIView, CreateGetTagsAPI

urlpatterns = [
    # url(r'(?P<tag_id>\d+)/images/?$', ,name='tag-images'),  # TODO: обриши имена
    url(r'(?P<tag_id>\d+)/?$', TagDetailAPIView.as_view(), name='detail'),  # TODO: обриши имена
    url(r'$', CreateGetTagsAPI.as_view(), name='list')

]


