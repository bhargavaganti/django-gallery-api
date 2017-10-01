from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from src.gallery.helpers import log
from .permissions import IsOwnerOrReadOnly, IsAdminOrOwner
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, \
    get_object_or_404
from .serializers import ProfileSerializer, CreateProfileSerializer, ProfileUpdateSerializer
from src.profiles.models import Profile


class GetProfilesAPI(ListAPIView):
    """
    Oво је прва АПИ класа у којој је потребно имплеменитрати
    добављање свих објеката, и њихово презентовање у JSON формату
    """
    serializer_class = ProfileSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    search_fields = ('user__username', 'user__first_name', 'user__email', 'timestamp', 'updated')
    ordering_fields = '__all__'

    def get_queryset(self, *args, **kwargs):
        queryset_list = Profile.objects.all()
        return queryset_list


class GetProfileAPI(RetrieveAPIView):
    """

    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # lookup_field = 'name' # ово се може користити уместо pk, дакле уместо albums/1 може albums/ime-albuma


class CreateProfileAPI(CreateAPIView):
    """

    """
    queryset = Profile.objects.all()
    serializer_class = CreateProfileSerializer
    permission_classes = [IsAuthenticated]


class UpdateProfileAPI(RetrieveUpdateAPIView):
    """

    """
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAdminOrOwner, ]

    #
    # def update(self, request, *args, **kwargs):
    #     print("\n\nInside update")
    #     serializer = ProfileSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     print(serializer.errors)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def put(self, request, *args, **kwargs):
    #     print("\n\nInside put")
    #     serializer = ProfileUpdateSerializer(self.get_object(),data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     print(serializer.errors)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #     # добршити ажурирање профила


    def put(self, request, *args, **kwargs):
        instance = Profile.objects.get(pk=kwargs.get("pk"))
        data = request.data
        if not instance:
            return Response(data={"status": "fail", "code": 404, "messages": ["No profile with that id"]})

        instance.user.first_name = data["user.first_name"] if data["user.first_name"] else instance.user.first_name
        instance.user.last_name = data["user.last_name"] if data["user.last_name"] else instance.user.last_name
        instance.user.email = data["user.email"] if data["user.email"] else instance.user.email
        instance.user.username = data["user.username"] if data["user.username"] else instance.user.username
        instance.user.is_active = bool(data["user.is_active"]) if data["user.is_active"] else instance.user.is_active
        instance.user.set_password(data["user.password"]) if data["user.password"] else instance.user.password
        instance.user.save()

        instance.profile_picture = data['profile_picture'] if data['profile_picture'] else instance.profile_picture
        instance.save()
        return instance


class DeleteProfileAPI(DestroyAPIView):
    """

    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrOwner, ]
