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
from .permissions import IsAdminOrOwnerOrReadOnly
from src.likes.models import Like
from src.profiles.models import Profile
from src.gallery.helpers import log
from src.images.models import Image


class CreateGetLikesAPI(ListAPIView, CreateAPIView):
    """

    """

    serializer_class = [LikeSerializer, CreateLikeSerializer]
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        self.serializer_class = LikeSerializer
        self.permission_classes = AllowAny

        image_id = self.kwargs.get("image_id")
        if not image_id:
            return JsonResponse({"status": "fail", "code": 403}, safe=True)

        image = Image.objects.get(pk=image_id)
        if not image:
            return JsonResponse({"status": "fail", "code": 404}, safe=True)

        queryset_list = Like.objects.filter(image__pk=image_id)
        return queryset_list

    def perform_create(self, serializer):
        if self.kwargs['profile_id']:
            profile = Profile.objects.get(user=self.request.user)
            serializer.save(owner=profile)

    def post(self, request, *args, **kwargs):
        self.permission_classes = IsAuthenticated
        self.serializer_class = CreateLikeSerializer

        image_id = self.kwargs.get('image_id')
        profile_id = Profile.objects.get(user=self.request.user).id

        if not image_id or not profile_id:
            return JsonResponse({"status": "fail", "code": 406})

        image = Image.objects.get(pk=self.kwargs.get('image_id'))
        profile = Profile.objects.get(user=self.request.user)

        # ако лајк већ постоји, обриши га
        try:
            exist = Like.objects.get(image__pk=image_id, owner__pk=profile_id)
            if exist:
                exist.delete()
                return JsonResponse({"status": "success", "code": 200, "data": None, "messages": ["Unliked!"]})
        except Like.DoesNotExist:
            pass

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
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def get_object(self):
        # ipdb.set_trace(context=5)
        image_id = self.kwargs.get("image_id")
        like_id = self.kwargs.get("like_id")

        if not (image_id and like_id):
            return JsonResponse({"status": "fail", "code": 406})

        image = Image.objects.get(pk=image_id)
        if not image:
            return JsonResponse({"status": "fail", "code": 404})

        like = image.like_set.get(pk=like_id)
        return like

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
