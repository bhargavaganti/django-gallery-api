from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, \
    get_object_or_404
from rest_framework.response import Response

from .serializers import LikeSerializer, CreateLikeSerializer
from src.likes.models import Like
from src.profiles.models import Profile
from src.gallery.helpers import log


class GetLikesAPI(ListAPIView):
    """

    """
    serializer_class = LikeSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!

    def get_queryset(self, *args, **kwargs):
        image_id = self.kwargs.get("image_id")
        if not image_id:
            queryset_list = Like.objects.all()
        queryset_list = Like.objects.filter(image__pk=image_id)
        if queryset_list.count() < 1:
            return Response({"status": "success"}, status=200)
        return queryset_list


class CreateLikeAPI(CreateAPIView):
    """

    """
    queryset = Like.objects.all()
    serializer_class = CreateLikeSerializer
    permission_classes = [IsAuthenticated]

    # FIXME: размисли да ли ово стављати
    # def perform_create(self, serializer):
    #     profile = Profile.objects.get(user=self.request.user)
    #     serializer.save(owner=profile)


class LikeDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        like_id = self.kwargs.get("like_id")
        if not like_id:
            return Response({"status": "fail"}, status=404)
        like = get_object_or_404(Like,pk=like_id)
        return like

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
