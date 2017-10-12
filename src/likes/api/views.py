import ipdb
from django.http import JsonResponse
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response

from src.albums.models import Album

from src.albums.api.permissions import IsOwnerOrReadOnly
from .serializers import LikeSerializer, CreateLikeSerializer, DetailedLikeSerializer
from src.likes.models import Like
from src.profiles.models import Profile
from src.gallery.helpers import log
from src.images.models import Image


class GetLikesAPI(ListAPIView):
    """

    """
    serializer_class = LikeSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        image_id = self.kwargs.get("image_id")
        if not image_id:
            return JsonResponse({"status": "fail", "code": 403}, safe=True)
        image = Image.objects.get(pk=image_id)
        if not image:
            return JsonResponse({"status": "fail", "code": 404}, safe=True)
        queryset_list = Like.objects.filter(image__pk=image_id)
        return queryset_list


class CreateLikeAPI(CreateAPIView):
    """

    """
    queryset = Like.objects.all()
    serializer_class = CreateLikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(owner=profile)

    def post(self, request, *args, **kwargs):
        image_id = self.kwargs.get('image_id')

        if not image_id:
            return JsonResponse({"status": "fail", "code": 406})
        image = Image.objects.get(pk=self.kwargs.get('image_id'))
        profile = Profile.objects.get(user=self.request.user)

        like = Like()
        like.save()
        like.owner.add(profile)
        like.image.add(image)
        like.save()

        return JsonResponse(self.serializer_class(instance=like).data)


class LikeDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Like.objects.all()
    serializer_class = DetailedLikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self):
        # ipdb.set_trace(context=5)
        profile_id = self.kwargs.get("profile_id")
        image_id = self.kwargs.get("image_id")
        like_id = self.kwargs.get("like_id")

        if not profile_id and image_id and like_id:
            return get_object_or_404(Like, pk=like_id)

        profile = Profile.objects.get(pk=profile_id)
        if not profile:
            return JsonResponse({"status":"fail","code":404})

        album_id = self.kwargs.get("album_id")
        album = Album.objects.get(pk=album_id)
        if not album:
            return JsonResponse({"status": "fail", "code": 404})

        image = Image.objects.get(pk=image_id)
        if not image:
            return JsonResponse({"status": "fail", "code": 404})

        if not like_id:
            return JsonResponse({"status": "fail", "code": 404})

        like = get_object_or_404(queryset=Like.objects.all(), pk=like_id, image__pk=image_id)
        return like

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
