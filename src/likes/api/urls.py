from django.conf.urls import url
from django.contrib import admin

from src.likes.api.views import GetLikesAPI, CreateLikeAPI, LikeDetailAPIView

urlpatterns = [
    url(r'(?P<like_id>\d+)/?$', LikeDetailAPIView.as_view(), name='detail'),
    url(r'create/?$', CreateLikeAPI.as_view(), name='create'),
    url(r'$', GetLikesAPI.as_view(), name='list')
]



