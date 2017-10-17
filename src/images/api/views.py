from django.db.models import Count
from django.http import JsonResponse, Http404
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, \
    get_object_or_404
import ipdb

from .serializers import ImageSerializer, CreateImageSerializer, DetailedImageSerializer
from src.images.models import Image
from src.profiles.models import Profile
from src.gallery.helpers import log, prepare_path
from src.albums.models import Album
from src.comments.models import Comment
from .permissions import IsOwnerOrReadOnly, IsAdminOrOwnerOrReadOnly


class CreateGetImagesAPI(ListAPIView, CreateAPIView):
    """
    Класа која се користи за креирање слике и за добављање листе
    свих слика репрезентованих у JSON формату
    """

    # класе за серијализацују које ће се применити
    serializer_class = ImageSerializer

    # класе права приступа
    permission_classes = [AllowAny]

    # укључивање могућности филтрирања
    filter_backends = [SearchFilter]  # ово мора бити низ!

    # поља по којима ће претрага бити вршена
    search_fields = ('name__icontains', 'description__icontains', 'tag__name__icontains', 'timestamp', 'updated')

    # начин сортирања резултата претраге
    ordering_fields = '__all__'


    def get_queryset(self, *args, **kwargs):
        """
        Метода помоћу које се добављају сви подаци
        :param   args:
        :param   kwargs:  album_id?, image_id
        :return: QuerySet
        """

        # ipdb.set_trace()

        # експлицитно назначавање која се серијализација користи
        self.serializer_class = ImageSerializer

        # узимање јединственог броја албума из URL-a
        album_id = self.kwargs.get("album_id", None)
        album = None

        # ако није постављен ид албума, врати све слике
        if album_id is None:
            return Image.objects.all()

        # узми објекат са ид-јем, ако не постоји врати 404
        album = get_object_or_404(Album,pk=album_id)

        # узимање свих слика из албума
        queryset_list = album.images.all()
        return queryset_list

    def post(self, request, *args, **kwargs):
        """
        Метода помоћу које се врши креирање
        Окида се на HTTP POST метод
        :param request: user, name, description, is_public, image,
        :param args:
        :param kwargs: album_id
        :return: Image|Http404
        """

        # ipdb.set_trace()

        # експлицитно назначавање која се серијализација користи
        serializer_class = CreateImageSerializer

        # експлицитно навођење која ће се класа за права приступа користити
        self.permission_classes = [IsAdminOrOwnerOrReadOnly] 

        # aко ид албума постоји у пољима POST захтева, узми га, ако не, узми из URL-a
        album_id = request.POST.get('album_id', self.kwargs.get('album_id', None))
        album    = get_object_or_404(Album, pk=album_id)
        
        # експлицитно проверавање права приступа, уколико нешто није у реду, баца се изузетак
        self.check_object_permissions(request, album)

        name        = request.POST.get('name', None)
        description = request.POST.get('description', None)
        is_public   = bool(request.POST.get('is_public', None))
        image       = request.FILES['image']

        # креирање слике
        image = Image.objects.create(
            name=name,
            description=description,
            is_public=is_public,
            image=image,
            album_id=album_id
        )
        # асоцијација са албумом
        album.images.add(image)
        album.save()
        return JsonResponse(serializer_class(instance=image).data)


class ImageDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """
    Класа која се користи за приказ, ажурирање и брисање инстанце класе Слика;
    Репрезентује податке у JSON формату
    """

    queryset           = Image.objects.all()
    serializer_class   = DetailedImageSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def get_object(self):
        """
        Метода помоћу које се врши добављање појединачне инстанце;
        Окида се на HTTP GET метод
        :return: Image|Http404
        """
        album_id = self.kwargs.get("album_id", None)
        image_id = self.kwargs.get("image_id", None)
        album = None

        if not album_id is None:
            album = get_object_or_404(Album, pk=album_id)
            return get_object_or_404(queryset=album.images.all(), pk=image_id)

        image = get_object_or_404(Image, pk=image_id)
        return image

    def put(self, request, *args, **kwargs):
        """
        Метода помоћу које се врши ажурирање инстанце;
        Окида се на HTTP POST метод;
        У овом случају, није потребно доћи до слике преко профила и албума,
        јер је слика видљива и преко путање /api/images/:id
        :param   request: user, name?, description?, is_public?, image?
        :param   args:
        :param   kwargs: image_id
        :return: Image|Http404
        """

         # TODO: ако се мења име слике, треба и на диску да се промени
        image_id = self.kwargs.get('image_id', None)
        image    = get_object_or_404(Image, pk=image_id)

        self.check_object_permissions(request, image)

        image.name        = request.POST.get('name', image.name)
        image.description = request.POST.get('description', image.description)
        image.is_public   = request.POST.get('is_public', image.is_public)
        image.image       = request.FILES.get('image', image.image)
        image.album       = request.POST.get('album', image.album)
        tags              = request.POST.getlist('tags', image.tag_set.all())

        # прођи кроз све тагове, и рекреирај асоцијације
        for tag in tags:
            try:
                image.tag_set.remove(tag)
                image.tag_set.add(tag)
            except:
                image.tag_set.add(tag)
        image.save()
        return JsonResponse(self.serializer_class(instance=image).data)


    def delete(self, request, *args, **kwargs):
        """
        Метода која се користи за брисање инстанце
        Окида се на HTTP DELETE методу
        :param request: user
        :param args:
        :param kwargs: image_id
        :return: JsonResponse
        """

        self.permission_classes = [IsAdminOrOwnerOrReadOnly]
        ipdb.set_trace()
        # користи се django-cleanup за брисање слике-датотеке

        image_id = self.kwargs.get('image_id', None)
        image    = get_object_or_404(Image, pk=image_id)

        self.check_object_permissions(request,image)

        # брисање свих асоцијација између слике и коментара
        image.comment_set.all().delete()

        # брисање свих коментара
        Comment.objects.filter(image__pk=image_id).delete()

        return self.destroy(request, *args, **kwargs)


class GetTopImages(ListAPIView):
    """
    Класа која се користи за приказ слика које
    имају исти или већи број лајкова од унапред
    дефинисаног у промењивој top_likes
    """
    serializer_class   = ImageSerializer
    filter_backends    = [SearchFilter]
    search_fields      = ('name__icontains', 'description__icontains', 'tag__name__icontains', 'timestamp', 'updated')
    ordering_fields    = '__all__'
    permission_classes = [AllowAny]

    def get_queryset(self):
        from src.gallery.settings import top_likes

        # селектовање свих слика које имају >= број лајкова него што је дефинисано у top_likes
        queryset_list = Image.objects.annotate(like__count=Count('like__pk')).filter(like__count__gte=top_likes)
        return queryset_list


class GetOwnerImages(ListAPIView):
    """
    Класа која служи за приказ свих слика које
    један профил има;
    """
    serializer_class   = ImageSerializer
    filter_backends    = [SearchFilter]  # ово мора бити низ!
    search_fields      = ('name__icontains', 'description__icontains', 'tag__name__icontains', 'timestamp', 'updated')
    ordering_fields    = '__all__'
    permission_classes = [AllowAny]

    def get_queryset(self):
        # ipdb.set_trace(context=5)
        profile_id = self.kwargs.get('profile_id', None)

        profile = get_object_or_404(Profile, pk=profile_id)

        # селектовање свих слика где је аутор албума наведени профил
        queryset = Image.objects.filter(album__owner__pk=profile_id)
        return queryset
