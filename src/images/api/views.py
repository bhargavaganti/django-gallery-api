from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny,IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from .serializers import ImageSerializer, CreateImageSerializer
from src.images.models import Image
from src.profiles.models import Profile


class GetImagesAPI(ListAPIView):
    """
    Oво је прва АПИ класа у којој је потребно имплеменитрати
    добављање свих објеката, и њихово презентовање у JSON формату
    """
    serializer_class = ImageSerializer
    filter_backends = [SearchFilter] # ово мора бити низ!
    search_fields = ('name', 'description', 'tag__name', 'timestamp', 'updated')
    ordering_fields = '__all__'

    def get_queryset(self, *args, **kwargs):
        queryset_list = Image.objects.all()
        return queryset_list


class GetImageAPI(RetrieveAPIView):
    """

    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    # lookup_field = 'name' # ово се може користити уместо pk, дакле уместо albums/1 може albums/ime-albuma


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

class UpdateImageAPI(RetrieveUpdateAPIView):
    """

    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # FIXME: размисли да ли ово стављати
    # def perform_create(self, serializer):
    #     profile = Profile.objects.get(user=self.request.user)
    #     serializer.save(owner=profile)


class DeleteImageAPI(DestroyAPIView):
    """

    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]