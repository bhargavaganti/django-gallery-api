from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from src.albums.models import Album
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, \
    get_object_or_404
from .serializers import ImageSerializer, CreateImageSerializer, DetailedImageSerializer
from src.images.models import Image
from src.profiles.models import Profile
from src.gallery.helpers import log
import ipdb


class GetImagesAPI(ListAPIView):
    """

    """
    serializer_class = ImageSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    search_fields = ('name', 'description', 'tag__name', 'timestamp', 'updated')
    ordering_fields = '__all__'
    lookup_field = 'image'

    def get_queryset(self, *args, **kwargs):
        # ipdb.set_trace()
        profile_id = self.kwargs.get("pk")
        if not profile_id:
            return Response({"status": "fail"}, status=403)

        profile = Profile.objects.get(pk=profile_id)

        album_id = self.kwargs.get("album_id")
        if not album_id:
            return Response({"status": "fail"}, status=403)

        queryset_list = Image.objects.filter(album_id=album_id)
        return queryset_list


class CreateImageAPI(CreateAPIView):
    """

    """
    queryset = Image.objects.all()
    serializer_class = CreateImageSerializer
    permission_classes = [IsAuthenticated]

    # FIXME: размисли да ли ово стављати
    # def perform_create(self, serializer):
    #     profile = Profile.objects.get(user=self.request.user)
    #     serializer.save(owner=profile)


class ImageDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Image.objects.all()
    serializer_class = DetailedImageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        album_id = self.kwargs.get("album_id")
        if not album_id:
            return Response({"status": "fail"}, status=403)
        album = Album.objects.get(pk=album_id)
        if not album:
            return Response({"status": "fail"}, status=404)

        image_id = self.kwargs.get("image_id")
        # return album.images.get(pk=image_id)
        return get_object_or_404(Image, pk=image_id, album_id=album_id)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
