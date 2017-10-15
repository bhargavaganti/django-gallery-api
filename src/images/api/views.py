from itertools import product

from django.db.models import Count
from django.http import JsonResponse, Http404
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from src.albums.models import Album

from .permissions import IsOwnerOrReadOnly, IsAdminOrOwnerOrReadOnly
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, \
    get_object_or_404
from .serializers import ImageSerializer, CreateImageSerializer, DetailedImageSerializer
from src.images.models import Image
from src.profiles.models import Profile
from src.gallery.helpers import log, prepare_path

import ipdb


class CreateGetImagesAPI(ListAPIView, CreateAPIView):
    """

    """
    serializer_class = [ImageSerializer, CreateImageSerializer]
    filter_backends = [SearchFilter]  # ово мора бити низ!
    search_fields = ('name__icontains', 'description__icontains', 'tag__name__icontains', 'timestamp', 'updated')
    ordering_fields = '__all__'
    lookup_field = 'image'
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        self.serializer_class = ImageSerializer
        # ipdb.set_trace()
        profile_id = self.kwargs.get("profile_id")
        album_id = self.kwargs.get("album_id")
        album = None

        if not profile_id and not album_id:
            return Image.objects.all()

        profile = Profile.objects.get(pk=profile_id)
        if not profile:
            return JsonResponse({"status": "fail"})

        if not album_id:
            return JsonResponse({"status": "fail"})

        album = profile.albums.get(pk=album_id)
        if not album:
            return JsonResponse({"status": "fail"})

        queryset_list = album.images.all()
        return queryset_list

    def post(self, request, *args, **kwargs):
        # ipdb.set_trace()
        serializer_class = CreateImageSerializer

        name = request.POST.get('name', None)
        description = request.POST.get('description', None)
        is_public = bool(request.POST.get('is_public', None))
        image = request.FILES['image']
        album_id = request.POST.get('album_id', self.kwargs.get('album_id'))

        image = Image.objects.create(
            name=name,
            description=description,
            is_public=is_public,
            image=image,
            album_id=album_id
        )
        return JsonResponse(serializer_class(instance=image).data)


class ImageDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Image.objects.all()
    serializer_class = DetailedImageSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly, IsAuthenticatedOrReadOnly]  #

    def get_object(self):
        album_id = self.kwargs.get("album_id")
        image_id = self.kwargs.get("image_id")
        album = None

        if album_id:
            try:
                album = Album.objects.get(pk=album_id)
            except:
                pass

            if image_id:
                try:
                    image = album.images.get(pk=image_id)
                    return image
                except:
                    raise Http404
                    # return JsonResponse({"status": "fail", "code": 404})
            else:
                raise Http404
                # return JsonResponse({"status":"fail","code":406})
        return get_object_or_404(Image, pk=image_id)

    def put(self, request, *args, **kwargs):
        """
        У овом случају, није потребно доћи до слике преко профила и албума,
        јер је слика видљива и преко путање /api/images/:id
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

         # TODO: ако се мења име слике, треба и на диску да се промени
        image_id = self.kwargs.get("image_id")

        image = Image.objects.get(pk=image_id)
        if not image:
            return Response({"status": "fail"}, status=404)

        image.name        = request.POST.get('name', image.name)
        image.description = request.POST.get('description', image.description)
        image.is_public   = request.POST.get('is_public', image.is_public)
        image.image       = request.FILES.get('image', image.image)
        image.album       = request.POST.get('album', image.album)
        tags              = request.POST.getlist('tags', image.tag_set.all())

        for tag in tags:
            try:
                image.tag_set.remove(tag)
                image.tag_set.add(tag)
            except:
                image.tag_set.add(tag)
        image.save()
        return JsonResponse(self.serializer_class(instance=image).data)

    def delete(self, request, *args, **kwargs):
        # користи се django-cleanup за брисање слике-датотеке
        return self.destroy(request, *args, **kwargs)


class GetTopImages(ListAPIView):
    serializer_class = ImageSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    search_fields = ('name', 'description', 'tag__name', 'timestamp', 'updated')
    ordering_fields = '__all__'
    lookup_field = 'image'
    permission_classes = [AllowAny]

    def get_queryset(self):
        from src.gallery.settings import top_likes

        queryset_list = Image.objects.annotate(like__count=Count('like__pk')).filter(like__count__gte=top_likes)
        return queryset_list


class GetOwnerImages(ListAPIView):
    serializer_class = ImageSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    search_fields = ('name', 'description', 'tag__name', 'timestamp', 'updated')
    ordering_fields = '__all__'
    lookup_field = 'image'
    permission_classes = [AllowAny]

    def get_queryset(self):
        # ipdb.set_trace(context=5)
        profile_id = self.kwargs.get("profile_id")
        if not profile_id:
            return ImageSerializer(None).data
        queryset = Image.objects.filter(album__owner__pk=profile_id)
        return queryset
