from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
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


class CreateProfileAPI(CreateAPIView):
    """

    """
    queryset = Profile.objects.all()
    serializer_class = CreateProfileSerializer
    permission_classes = [AllowAny]
    # треба уградити captcha код


class ProfileDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrOwner, ]

    def get_object(self):
        return Profile.objects.get(pk=self.kwargs.get("profile_id"))

    def put(self, request, *args, **kwargs):
        # instance = Profile.objects.get(pk=kwargs.get("pk"))
        instance = self.get_object()
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

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
