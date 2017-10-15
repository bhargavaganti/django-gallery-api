from django.conf.urls import url
from django.contrib import admin

from src.likes.api.views import CreateGetLikesAPI, LikeDetailAPIView

urlpatterns = [
    url(r'(?P<like_id>\d+)/?$', LikeDetailAPIView.as_view(), name='detail'),
    url(r'$', CreateGetLikesAPI.as_view(), name='list-create')
]



