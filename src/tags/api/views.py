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
    Класа која се користи за креирање ознаке и за добављање листе
    свих ознака репрезентованих у JSON формату
    """

    # класе за серијализацују које ће се применити
    serializer_class   = TagSerializer

    # укључивање могућности филтрирања
    filter_backends    = [SearchFilter]  # ово мора бити низ!

    # поља по којима ће претрага бити вршена
    search_fields      = ('name__icontains',)

    # начин сортирања резултата претраге
    ordering_fields    = 'name'

    # класе права приступа
    permission_classes = [AllowAny]


    def get_queryset(self, *args, **kwargs):
        """
        Метода помоћу које се добављају сви подаци
        :param   args:
        :param   kwargs:  image_id?
        :return: QuerySet
        """

        image_id = self.kwargs.get("image_id", None)

        if not image_id:
            return Tag.objects.all()

        queryset_list = Image.objects.get(pk=image_id).tag_set.all()
        return queryset_list


    def post(self, request, *args, **kwargs):
        """
        Метода помоћу које се врши креирање
        Окида се на HTTP POST метод
        :param request: user, name
        :param args:
        :param kwargs: tag_id
        :return: Tag|Http404
        """

        self.serializer_class   = CreateTagSerializer
        self.permission_classes = [IsAuthenticated]
        return self.create(request,*args, **kwargs)


class TagDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """
    Класа која се користи за приказ, ажурирање и брисање инстанце класе Ознака;
    Репрезентује податке у JSON формату
    """

    queryset = Tag.objects.all()
    serializer_class   = DetailedTagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        """
        Метода помоћу које се врши добављање појединачне инстанце;
        Окида се на HTTP GET метод
        :return: Tag|Http404
        """
        image_id = self.kwargs.get("image_id", None)
        tag_id   = self.kwargs.get("tag_id", None)

        if image_id is None:
            # узми објекат са ид-јем, ако не постоји врати 404
            return get_object_or_404(Tag, pk=tag_id)

        image = get_object_or_404(Image, pk=image_id)
        return get_object_or_404(image.tag_set.all(), pk=tag_id)

    def put(self, request, *args, **kwargs):
        """
        Метода помоћу које се врши ажурирање инстанце;
        Окида се на HTTP PUT метод;
        :param   request: user, name?
        :param   args:
        :param   kwargs: tag_id
        :return: Tag|Http404
        """

        tag_id = self.kwargs.get("tag_id", None)
        tag    = get_object_or_404(Tag, pk=tag_id)

        self.check_object_permissions(request, tag)
        return self.update(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        """
        Метода која се користи за брисање инстанце
        Окида се на HTTP DELETE методу
        :param   request: user
        :param   args:
        :param   kwargs: tag_id
        :return: JsonResponse
        """

        tag_id = self.kwargs.get("tag_id", None)
        tag    = get_object_or_404(Tag, pk=tag_id)

        self.check_object_permissions(request, tag)
        return self.destroy(request, *args, **kwargs)
