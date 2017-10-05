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


class GetAllImages(ListAPIView):
    """

    """
    serializer_class = ImageSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    search_fields = ('name', 'description', 'tag__name', 'timestamp', 'updated')
    ordering_fields = '__all__'
    lookup_field = 'image'
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Image.objects.filter(album_id=self.kwargs.get("album_id")) or Image.objects.all()


class GetImage(RetrieveAPIView):
    """

    """
    queryset = Image.objects.all()
    serializer_class = DetailedImageSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return Image.objects.get(pk=self.kwargs.get("image_id"))


class GetImagesAPI(ListAPIView):
    """

    """
    serializer_class = ImageSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    search_fields = ('name', 'description', 'tag__name', 'timestamp', 'updated')
    ordering_fields = '__all__'
    lookup_field = 'image'
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        # ipdb.set_trace()
        profile_id = self.kwargs.get("profile_id")
        if not profile_id:
            # return Image.objects.all()
            return Response({"status": "fail"}, status=403)

        profile = Profile.objects.get(pk=profile_id)

        if not profile:
            return Response({"status": "fail"}, status=404)

        album_id = self.kwargs.get("album_id")
        if not album_id:
            # return Image.objects.all()
            return Response({"status": "fail"}, status=403)

        album = Album.objects.get(pk=album_id, owner_id=profile_id)
        if not album:
            return Response({"status": "fail"}, status=404)

        queryset_list = Image.objects.filter(album_id=album_id)
        return queryset_list


class CreateImageAPI(CreateAPIView):
    """

    """
    queryset = Image.objects.all()
    serializer_class = CreateImageSerializer
    permission_classes = [IsAuthenticated]


class ImageDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Image.objects.all()
    serializer_class = DetailedImageSerializer
    permission_classes = [ IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] # FIXME: testiraj

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
