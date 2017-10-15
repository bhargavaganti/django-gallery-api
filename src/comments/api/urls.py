from django.conf.urls import url
from django.contrib import admin

from src.comments.api.views import CreateGetCommentsAPI, CommentDetailAPIView

urlpatterns = [
    url(r'(?P<comment_id>\d+)/?$', CommentDetailAPIView.as_view(), name='detail'),
    url(r'$', CreateGetCommentsAPI.as_view(), name='list-create'),
]




