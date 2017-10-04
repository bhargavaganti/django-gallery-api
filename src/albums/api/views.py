from django.http import JsonResponse
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from src.gallery.helpers import log
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, \
    get_object_or_404
from src.albums.models import Album
from .serializers import AlbumSerializer, CreateAlbumSerializer, DetailedAlbumSerializer
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
        # ipdb.set_trace()
        pk = self.kwargs.get("pk")
        if not pk:
            return JsonResponse({"status": "fail", "code": 403}, safe=True)

        profile = Profile.objects.get(pk=pk)
        if not profile:
            return JsonResponse({"status":"fail", "code":404}, safe=True)

        queryset_list = Album.objects.filter(owner_id=pk)
        return queryset_list


class CreateAlbumAPI(CreateAPIView):
    """

    """
    queryset = Album.objects.all()
    serializer_class = CreateAlbumSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     profile = Profile.objects.get(user=self.request.user) # FIXME: можда је боље укључити у продукцији
    #     serializer.save(owner=profile)


class AlbumDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Album.objects.all()
    serializer_class = DetailedAlbumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]

    def get_object(self):
        profile_id = self.kwargs.get("pk")
        profile = Profile.objects.get(pk=profile_id)
        album = None

        if not profile:
            return JsonResponse({"status:": "fail"}, safe=True)

        album_id = self.kwargs.get("album_id")

        # album = Album.objects.get(pk=album_id, owner_id=profile_id)
        album = get_object_or_404(Album, pk=album_id, owner_id=profile_id)
        return album

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
