import ipdb
from django.http import JsonResponse
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response

from src.albums.models import Album

from src.albums.api.permissions import IsOwnerOrReadOnly
from .serializers import LikeSerializer, CreateLikeSerializer, DetailedLikeSerializer
from .permissions import IsAdminOrOwnerOrReadOnly
from src.likes.models import Like
from src.profiles.models import Profile
from src.gallery.helpers import log
from src.images.models import Image


class CreateGetLikesAPI(ListAPIView, CreateAPIView):
    """
    Класа која се користи за креирање лајка и за добављање листе
    свих лајкова репрезентованих у JSON формату
    """

    # класе за серијализацују које ће се применити
    serializer_class   = LikeSerializer

    # класе права приступа
    permission_classes = [AllowAny]


    def get_queryset(self, *args, **kwargs):
        """
        Метода помоћу које се добављају сви подаци
        :param args:
        :param kwargs:  image_id
        :return: QuerySet
        """

        # експлицитно назначавање која се серијализација користи
        self.serializer_class = LikeSerializer

        image_id = self.kwargs.get("image_id")

        # узми објекат са ид-јем, ако не постоји врати 404
        image = get_object_or_404(Image, pk=image_id)

        # добављање свих лајкова који су асоцијацији са сликом
        queryset_list = image.like_set.all()
        return queryset_list



    def post(self, request, *args, **kwargs):
        """
        Метода помоћу које се врши креирање
        Окида се на HTTP POST метод
        :param request: user
        :param args:
        :param kwargs: image_id
        :return: Like|Http404
        """

        # експлицитно навођење која ће се класа за права приступа користити
        self.permission_classes = [IsAuthenticated]

        self.serializer_class   = CreateLikeSerializer

        image_id = self.kwargs.get('image_id', None)
        image = get_object_or_404(Image, image_id)

        profile = get_object_or_404(Profile, user=self.request.user)

        # ако лајк већ постоји, обриши га
        try:
            exist = Like.objects.get(image__pk=image_id, owner__pk=profile.id)
            if exist:
                exist.delete()
                return JsonResponse({"status": "success", "code": 200, "data": None, "messages": ["Unliked!"]})
        except Like.DoesNotExist:
            pass

        like = Like()
        like.save()
        # асоцијација са профилом
        like.owner.add(profile)
        # асоцијација са сликом
        like.image.add(image)
        like.save()

        return JsonResponse(self.serializer_class(instance=like).data)


class LikeDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """
    Класа која се користи за приказ, ажурирање и брисање инстанце класе Лајк;
    Репрезентује податке у JSON формату
    """
    queryset = Like.objects.all()
    serializer_class = DetailedLikeSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def get_object(self):
        """
        Метода помоћу које се врши добављање појединачне инстанце;
        Окида се на HTTP GET метод
        :return: Like|Http404
        """
        # ipdb.set_trace(context=5)
        image_id = self.kwargs.get("image_id", None)
        like_id  = self.kwargs.get("like_id", None)

        image = get_object_or_404(Image, pk=image_id)
        like  = get_object_or_404(queryset=image.like_set.all(), pk=like_id)
        return like

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
