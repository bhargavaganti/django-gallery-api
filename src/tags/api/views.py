import ipdb
from rest_framework.decorators import detail_route
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, \
    get_object_or_404
from rest_framework.response import Response

from src.images.api.serializers import DetailedImageSerializer
from .serializers import TagSerializer, CreateTagSerializer, DetailedTagSerializer
from src.tags.models import Tag
from src.profiles.models import Profile
from src.gallery.helpers import log
from src.images.models import Image


class CreateGetTagsAPI(ListAPIView, CreateAPIView):
    """

    """
    serializer_class   = TagSerializer
    filter_backends    = [SearchFilter]  # ово мора бити низ!
    search_fields      = ('name',)
    ordering_fields    = 'name'
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        image_id = self.kwargs.get("image_id")

        if not image_id:
            queryset_list = Tag.objects.all()
            return queryset_list

        queryset_list = Image.objects.get(pk=image_id).tag_set.all()
        return queryset_list

    def post(self, request, *args, **kwargs):
        self.serializer_class   = CreateTagSerializer
        self.permission_classes = IsAuthenticated
        return self.create(request,*args, **kwargs)


class TagDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Tag.objects.all()
    serializer_class   = DetailedTagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        image_id = self.kwargs.get("image_id")
        tag_id   = self.kwargs.get("tag_id")

        if not image_id:
            if not tag_id:
                return Response({"status": "fail"}, status=406)
            return get_object_or_404(Tag, pk=tag_id)
        return get_object_or_404(Image.objects.get(pk=image_id).tag_set.all(), pk=tag_id)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
