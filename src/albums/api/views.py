from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny,IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from .serializers import AlbumSerializer, CreateAlbumSerializer
from src.albums.models import Album
from src.profiles.models import Profile


class GetAlbumsAPI(ListAPIView):
    """
    Oво је прва АПИ класа у којој је потребно имплеменитрати
    добављање свих објеката, и њихово презентовање у JSON формату
    """
    serializer_class = AlbumSerializer
    filter_backends = [SearchFilter] # ово мора бити низ!
    search_fields = ('name', 'description', 'owner__user__username', 'timestamp', 'updated')
    ordering_fields = '__all__'

    def get_queryset(self, *args, **kwargs):
        queryset_list = Album.objects.all()
        return queryset_list


class GetAlbumAPI(RetrieveAPIView):
    """

    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    # lookup_field = 'name' # ово се може користити уместо pk, дакле уместо albums/1 може albums/ime-albuma


class CreateAlbumAPI(CreateAPIView):
    """

    """
    queryset = Album.objects.all()
    serializer_class = CreateAlbumSerializer
    permission_classes = [IsAuthenticated]

    # FIXME: размисли да ли ово стављати
    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(owner=profile)

class UpdateAlbumAPI(RetrieveUpdateAPIView):
    """

    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # FIXME: размисли да ли ово стављати
    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(owner=profile)


class DeleteAlbumAPI(DestroyAPIView):
    """

    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]