import ipdb
from django.http import JsonResponse
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.response import Response

from .serializers import CommentSerializer, CreateCommentSerializer, DetailedCommentSerializer
from src.comments.models import Comment
from src.profiles.models import Profile
from src.gallery.helpers import log
from src.albums.models import Album
from src.images.models import Image


class GetCommentsAPI(ListAPIView):
    """

    """
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    authentication_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
       # ipdb.set_trace(context=5)
        profile_id = self.kwargs.get("profile_id")
        if not profile_id:
            return Response({"status": "fail"}, status=403)

        profile = Profile.objects.get(pk=profile_id)

        album_id = self.kwargs.get("album_id")
        if not album_id:
            return Response({"status": "fail"}, status=403)
        album = Album.objects.get(pk=album_id, owner_id=profile_id)

        if not album:
            return Response({"status": "fail"}, status=404)

        image_id = self.kwargs.get("image_id")
        if not image_id:
            return Response({"status": "fail"}, status=403)
        image = Image.objects.get(pk=image_id, album_id=album_id)

        queryset_list = Comment.objects.filter(image__pk=image_id)
        return queryset_list


class CreateCommentAPI(CreateAPIView):
    """

    """
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(owner=profile)


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Comment.objects.all()
    serializer_class = DetailedCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        profile_id = self.kwargs.get("profile_id")
        profile = Profile.objects.get(pk=profile_id)
        if not profile:
            return JsonResponse({"status":"fail","code":404})

        album_id = self.kwargs.get("album_id")
        album = Album.objects.get(pk=album_id)
        if not album:
            return JsonResponse({"status": "fail", "code": 404})

        image_id = self.kwargs.get("image_id")
        image = Image.objects.get(pk=image_id)
        if not image:
            return JsonResponse({"status": "fail", "code": 404})

        comment_id = self.kwargs.get("comment_id")
        if not comment_id:
            return JsonResponse({"status": "fail", "code": 404})

        comment = get_object_or_404(queryset=Comment.objects.all(), pk=comment_id, image__pk=image_id)
        return comment

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
