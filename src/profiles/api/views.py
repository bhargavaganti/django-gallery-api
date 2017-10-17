import ipdb
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from src.gallery.helpers import log
from .permissions import IsOwnerOrReadOnly, IsAdminOrOwnerOrReadOnly
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, \
    get_object_or_404
from .serializers import ProfileSerializer, CreateProfileSerializer, ProfileUpdateSerializer
from src.profiles.models import Profile
from src.albums.models import Album
from src.comments.models import Comment
from src.likes.models import Like


class CreateGetProfilesAPI(ListAPIView, CreateAPIView):
    """
    Класа која се користи за креирање лајка и за добављање листе
    свих Профила репрезентованих у JSON формату
    """

    # класе за серијализацују које ће се применити
    serializer_class = ProfileSerializer

    # класе права приступа
    permission_classes = [AllowAny]

    # укључивање могућности филтрирања
    filter_backends = [SearchFilter]  # ово мора бити низ!

    # поља по којима ће претрага бити вршена
    search_fields    = ('user__username__icontains', 'user__first_name__icontains', 'user__email__icontains', 'timestamp', 'updated')

    # начин сортирања резултата претраге
    ordering_fields  = '__all__'


    def get_queryset(self, *args, **kwargs):
        """
        Метода помоћу које се добављају сви подаци
        :param   args:
        :param   kwargs:
        :return: QuerySet
        """
        queryset_list = Profile.objects.all()
        return queryset_list


    def post(self, request, *args, **kwargs):
        """
        Метода помоћу које се врши креирање
        Окида се на HTTP POST метод
        :param   request: user, user.first_name?, user.last_name?,
        user.username, user.email, user.is_active, user.password, profile_picture
        :param   args:
        :param   kwargs:
        :return: Profile|Http404
        """

        # експлицитно назначавање која се серијализација користи
        self.serializer_class   = CreateProfileSerializer
        # позивање методе create из CreateProfileSerializer-a
        return self.create(request, *args, **kwargs)


class ProfileDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """
    Класа која се користи за приказ, ажурирање и брисање инстанце модела Профил;
    Репрезентује податке у JSON формату
    """

    queryset           = Profile.objects.all()
    serializer_class   = ProfileUpdateSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]


    def get_object(self):
        """
        Метода помоћу које се врши добављање појединачне инстанце;
        Окида се на HTTP GET метод
        :return: Profile|Http404
        """

        profile_id = self.kwargs.get("profile_id", None)

        # узми објекат са ид-јем, ако не постоји врати 404
        return get_object_or_404(Profile, pk=profile_id)

    def put(self, request, *args, **kwargs):
        """
        Метода помоћу које се врши ажурирање инстанце;
        Окида се на HTTP POST метод;
        :param   request: user, user.first_name?, user.last_name?,
        user.username?, user.email?, user.is_active?, user.password?, profile_picture?
        :param   args:
        :param   kwargs: profile_id
        :return: Profile|Http404
        """

        # ipdb.set_trace()
        profile_id = self.kwargs.get("profile_id", None)
        instance = get_object_or_404(Profile, pk=profile_id)

        # експлицитно проверавање права приступа, уколико нешто није у реду, баца се изузетак
        self.check_object_permissions(request,instance)

        data = request.data
        instance.user.first_name = data.get('user.first_name', instance.user.first_name)
        instance.user.last_name  = data.get('user.last_name',  instance.user.last_name)
        instance.user.email      = data.get('user.email',      instance.user.email)
        instance.user.username   = data.get('user.username',   instance.user.username)
        instance.user.is_active  = data.get('user.is_active',  instance.user.is_active)
        instance.profile_picture = data.get('profile_picture', instance.profile_picture)

        if 'user.password' in data:
            instance.user.set_password(data['user.password'])
        instance.user.save()
        instance.save()

        return JsonResponse(self.serializer_class(instance=instance).data)


    def delete(self, request, *args, **kwargs):
        """
        Метода која се користи за брисање инстанце
        Окида се на HTTP DELETE методу
        :param   request: user
        :param   args:
        :param   kwargs: profile_id
        :return: JsonResponse
        """

        profile_id = self.kwargs.get("profile_id", None)
        profile = get_object_or_404(Profile, pk=profile_id)

        self.check_object_permissions(request,profile)

        # брисање свих асоцијација између албума и профила
        profile.albums.all().delete()

        # брисање албума
        Album.objects.filter(profile__pk=profile_id).delete()

        # брисање корисника
        profile.user.delete()

        profile.delete()

        return JsonResponse({"status":"success"})
        # return self.destroy(request, *args, **kwargs)
