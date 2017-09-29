from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny,IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from .serializers import TagSerializer, CreateTagSerializer
from src.tags.models import Tag
from src.profiles.models import Profile


class GetTagsAPI(ListAPIView):
    """

    """
    serializer_class = TagSerializer
    filter_backends = [SearchFilter] # ово мора бити низ!
    search_fields = ('name', )
    ordering_fields = 'name'

    def get_queryset(self, *args, **kwargs):
        queryset_list = Tag.objects.all()
        return queryset_list


class GetTagAPI(RetrieveAPIView):
    """

    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # lookup_field = 'name' # ово се може користити уместо pk, дакле уместо tags/1 може tags/ime-albuma


class CreateTagAPI(CreateAPIView):
    """

    """
    queryset = Tag.objects.all()
    serializer_class = CreateTagSerializer
    permission_classes = [IsAuthenticated]

    # FIXME: размисли да ли ово стављати
    # def perform_create(self, serializer):
    #     profile = Profile.objects.get(user=self.request.user)
    #     serializer.save(owner=profile)

# class UpdateTagAPI(RetrieveUpdateAPIView):
#     """
#
#     """
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#
#     # FIXME: размисли да ли ово стављати
#     # def perform_create(self, serializer):
#     #     profile = Profile.objects.get(user=self.request.user)
#     #     serializer.save(owner=profile)


class DeleteTagAPI(DestroyAPIView):
    """

    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]
