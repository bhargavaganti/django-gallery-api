import json
import os
from django.http import JsonResponse, HttpResponse
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, \
    get_object_or_404
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from src.albums.models import Album
from src.gallery.helpers import log
from src.gallery.settings import MEDIA_ROOT

from src.albums.api.permissions import IsOwnerOrReadOnly
from .serializers import AlbumSerializer, CreateAlbumSerializer, DetailedAlbumSerializer
from src.profiles.models import Profile
from src.profiles.api.permissions import IsAdminOrOwner
from src.images.api.serializers import CreateImageSerializer
from src.images.models import Image
from src.gallery.helpers import prepare_path
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
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        profile_id = self.kwargs.get("profile_id")
        if not profile_id:
            return Album.objects.all()

        profile = Profile.objects.get(pk=profile_id)
        if not profile:
            return JsonResponse({"status": "fail", "code": 404}, safe=True)

        queryset_list = Album.objects.filter(owner_id=profile_id)
        return queryset_list


class CreateAlbumAPI(CreateAPIView):
    """

    """

    queryset = Album.objects.all()
    serializer_class = CreateAlbumSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)  # TODO: тестирати
            serializer.save(owner=profile)

    def post(self, request, *args, **kwargs):
        profile_id = request.user if request.user.is_authenticated else request.POST['owner']
        profile = Profile.objects.get(pk=profile_id)
        album_name = prepare_path(request.POST['name'])
        description = request.POST['description'] or ""
        public = request.POST['is_public']

        album = Album.objects.create(
            name=album_name,
            description=description,
            owner=profile,
            is_public=public
        )

        images = []
        image_files = request.FILES.getlist('images')

        for img_file in image_files:
            img_file.name = prepare_path(img_file)
            image = {'name': img_file.name, 'image': img_file, 'is_public': public}
            images.append(image)
        album.save()

        for img in images:
            img['album_id'] = album.id
            image = Image.objects.create(
                name=img['name'],
                album_id=img['album_id'],
                is_public=img['is_public'],
                image=img['image']
            )
            image.save()
            album.images.add(image)

        album.save()
        serializer = self.serializer_class(instance=album)
        return JsonResponse(serializer.data)


class AlbumDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Album.objects.all()
    serializer_class = DetailedAlbumSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    # authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self):
        profile_id = self.kwargs.get("profile_id")
        album = None
        album_id = self.kwargs.get("album_id")

        if not profile_id:
            album = get_object_or_404(Album, pk=album_id)
            return album

        profile = Profile.objects.get(pk=profile_id)
        if profile:
            album = get_object_or_404(Album, pk=album_id, owner_id=profile_id)
        return album

    def put(self, request, *args, **kwargs):
        # TODO: ако се мења име албума, треба и на диску да се промени
        album       = Album.objects.get(pk=kwargs['album_id'])
        name        = request.POST['name']
        description = request.POST['description']
        images      = request.FILES.getlist('images')
        is_public   = request.POST['is_public']
        owner_id    = request.POST['owner']
        owner = None

        if owner_id:
            profile = Profile.objects.get(pk=owner_id)

        album.name        = name if name else album.name
        album.description = description if description else album.description
        album.images      = images if not images else album.images
        album.is_public   = is_public if is_public is not None else album.is_public
        album.owner       = owner if owner is not None else album.owner
        album.save()

        serializer = self.serializer_class(instance=album)
        return JsonResponse(serializer.data)

        # return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        import shutil

        album = Album.objects.get(pk=kwargs['album_id'])
        name = prepare_path(album.name)
        try:
            shutil.rmtree(MEDIA_ROOT + "/img/" + name + "/")
        except Exception as e:
            log("Error while removing album files: " + str(e))
        images = album.images.all()
        for img in images:
            img.delete()
        return self.destroy(request, *args, **kwargs)
