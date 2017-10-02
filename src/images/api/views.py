from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter

from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny,IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from .serializers import ImageSerializer, CreateImageSerializer
from src.images.models import Image
from src.profiles.models import Profile
from src.gallery.helpers import log
import ipdb

class GetImagesAPI(ListAPIView):
    """

    """
    serializer_class = ImageSerializer
    filter_backends = [SearchFilter] # ово мора бити низ!
    search_fields = ('name', 'description', 'tag__name', 'timestamp', 'updated')
    ordering_fields = '__all__'
    lookup_field = 'image'

    def get_queryset(self, *args, **kwargs):
       # ipdb.set_trace()
        log(self.kwargs)
        album_id = self.kwargs.get("pk")
        if not album_id:
            queryset_list = Image.objects.all()
        queryset_list = Image.objects.filter(album__pk=album_id)
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
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
