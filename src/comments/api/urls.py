from django.conf.urls import url
from django.contrib import admin

from src.comments.api.views import GetCommentsAPI, CommentDetailAPIView, CreateCommentAPI

urlpatterns = [
    url(r'(?P<comment_id>\d+)/$', CommentDetailAPIView.as_view(), name='all-comments'),
    url(r'create/?$', CreateCommentAPI.as_view(), name='create'),
    url(r'$', GetCommentsAPI.as_view(), name='comment'),
]




