from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from src.gallery.helpers import log
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from .serializers import AlbumSerializer, CreateAlbumSerializer
from src.albums.models import Album
from src.profiles.models import Profile
from src.profiles.api.permissions import IsAdminOrOwner
import ipdb


class GetAlbumsAPI(ListAPIView):
    """
    Oво је прва АПИ класа у којој је потребно имплеменитрати
    добављање свих објеката, и њихово презентовање у JSON формату
    """
    serializer_class = AlbumSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    search_fields = ('name', 'description', 'owner__user__username', 'timestamp', 'updated')
    ordering_fields = '__all__'

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if not pk:
            queryset_list = Album.objects.filter(owner__pk=pk)
        queryset_list = Album.objects.all()
        return queryset_list


class CreateAlbumAPI(CreateAPIView):
    """

    """
    queryset = Album.objects.all()
    serializer_class = CreateAlbumSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(owner=profile)


class AlbumDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]

    # def get(self, request, *args, **kwargs):
    #     profile = Profile.objects.get(pk=self.kwargs.get("pk"))
    #     album = None
    #     if not profile:
    #         return Response({"status":"fail", "code": 404})
    #
    #     album_id = self.kwargs.get("album_id")
    #     if not album_id:
    #         album = Response(self.get_object())
    #     if self.request.user.is_superuser:
    #         album = Response(Album.objects.get(pk=album_id))
    #     album = profile.albums.filter(pk=album_id)
    #     log(album)
    #     serializer = (album)
    #     return Response(serializer.data)

    def get_object(self):
        profile_id = self.kwargs.get("pk")
        profile = Profile.objects.get(pk=profile_id)
        album = None
        if not profile:
            log("no profile")
            return Response({"status:": "fail"}, status=404)
        album_id = self.kwargs.get("album_id")
        if self.request.user.is_superuser:
            album = Album.objects.get(pk=album_id)
        else:
            album = profile.albums.get(pk=album_id)
        return album

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
