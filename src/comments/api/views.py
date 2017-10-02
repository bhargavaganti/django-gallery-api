import ipdb
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from .serializers import CommentSerializer, CreateCommentSerializer
from src.comments.models import Comment
from src.profiles.models import Profile
from src.gallery.helpers import log


class GetCommentsAPI(ListAPIView):
    """

    """
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!

    def get_queryset(self, *args, **kwargs):
        # ipdb.set_trace()
        # get all Comments from image, if is set
        image_id = self.kwargs.get("image_id")
        if not image_id:
            queryset_list = Comment.objects.all()
        queryset_list = Comment.objects.filter(image__pk=image_id)
        if queryset_list.count() < 1:
            return Response({"status": "success"}, status=200)
        return queryset_list


class CreateCommentAPI(CreateAPIView):
    """

    """
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]

    # FIXME: размисли да ли ово стављати
    # def perform_create(self, serializer):
    #     profile = Profile.objects.get(user=self.request.user)
    #     serializer.save(owner=profile)


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        comment_id = self.kwargs.get("comment_id")
        if not comment_id:
            return Response({"status": "fail"}, status=404)
        comment = Comment.objects.get(pk=comment_id)
        return comment

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
