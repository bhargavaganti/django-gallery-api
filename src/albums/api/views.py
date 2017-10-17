import os
from django.http import JsonResponse, Http404
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, \
    get_object_or_404

from src.albums.models import Album
from src.gallery.helpers import log
from src.gallery.settings import MEDIA_ROOT
from src.albums.api.permissions import IsAdminOrOwnerOrReadOnly
from .serializers import AlbumSerializer, CreateAlbumSerializer, DetailedAlbumSerializer
from src.profiles.models import Profile
from src.images.models import Image
from src.gallery.helpers import prepare_path
import ipdb


class CreateGetAlbumsAPI(ListAPIView, CreateAPIView):
    """
    Класа која се користи за креирање албума и за добављање листе
    свих албума презентованих у JSON формату
    """

    # класе за серијализацују које ће се применити
    serializer_class = AlbumSerializer

    # укључивање могућности филтрирања
    filter_backends = [SearchFilter]  # ово мора бити низ!

    # поља по којима ће претрага бити вршена
    search_fields = ('name__icontains', 'description__icontains', 'owner__user__username__icontains', 'timestamp', 'updated')

    # начин сортирања резултата претраге
    ordering_fields = '__all__'

    # класе права приступа
    permission_classes = [AllowAny]

    # класе за обраду датотека
    parser_classes = (MultiPartParser, FormParser,JSONParser,)


    def get_queryset(self, *args, **kwargs):
        """
        Метода помоћу које се добављају сви подаци
        :param args:
        :param kwargs: profile_id? , album_id
        :return: QuerySet
        """
        # експлицитно назначавање која се серијализација користи
        self.serializer_class = AlbumSerializer

        # узимање јединственог броја профила из URL-a
        profile_id = self.kwargs.get("profile_id", None)

        # ако није постављен ид профила, врати све слике
        if not profile_id:
            queryset_list = Album.objects.all()
            return queryset_list

        # ако профил постоји, узми га
        profile = get_object_or_404(Profile, pk=profile_id)

        # ако профил постоји, врати све албуме профила
        queryset_list = profile.albums.all()
        return queryset_list


    def post(self, request, *args, **kwargs):
        """
        Метода помоћу које се врши креирање
        Окида се на HTTP POST метод
        :param request: user, name, description, is_public, images?,
        :param args:
        :param kwargs: profile_id
        :return: Album|Http404
        """

        self.serializer_class   = CreateAlbumSerializer

        # експлицитно навођење која ће се класа за права приступа користити
        self.permission_classes = [IsAuthenticated]
        profile    = None

        # узимање података о профилу из захтева
        profile = get_object_or_404(Profile, user=self.request.user)

        album_name  = request.POST['name']
        description = request.POST['description'] or ""
        public      = request.POST['is_public']

        # креирање албума
        album = Album.objects.create(
            name=album_name,
            description=description,
            is_public=public
        )
        album.save()

        images = []
        # узимање листе фајлова из захтева
        image_files = request.FILES.getlist('images')

        # креирање низа речника са свим информацијама о слици
        for img_file in image_files:
            img_file.name = prepare_path(img_file)
            image = {'name': img_file.name, 'image': img_file, 'is_public': public}
            images.append(image)

        # итерација кроз низ података о слици и креирање објеката слике
        for img in images:
            img['album_id'] = album.id
            image = Image.objects.create(
                name=img['name'],
                album_id=img['album_id'],
                is_public=img['is_public'],
                image=img['image']
            )
            image.save()

            # асоцијација са албумом
            album.images.add(image)

        album.save()

        # асоцијација са профилом - креатором
        profile.albums.add(album)
        profile.save()

        # серијализација података
        serializer = self.serializer_class(instance=album)
        return JsonResponse(serializer.data)


class AlbumDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """
    Класа која се користи за приказ, ажурирање и брисање инстанце класе Албум;
    Репрезентује податке у JSON формату
    """
    queryset           = Album.objects.all()
    serializer_class   = DetailedAlbumSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]


    def get_object(self):
        """
        Mетода која се користи за добијање појединачног објекта
        Окида се на HTTP GET методу
        :return: Album | Http404
        """
        from rest_framework.response import Response

        profile_id = self.kwargs.get('profile_id', None)
        album_id   = self.kwargs.get('album_id', None)
        album      = None

        if album_id is None:
            raise Http404

        # aко не постоји профил, узми албум непосредно
        if profile_id:
            album = get_object_or_404(Album,pk=album_id)
            return album

        profile = get_object_or_404(Profile,pk=profile_id)

        # ако постоји профил, узуми албум из његове колекције
        album = get_object_or_404(queryset=profile.albums.all(),pk=album_id)
        return album

    def put(self, request, *args, **kwargs):
        """
        Метода која се користи за ажурирање објекта
        Окида се на HTTP PUT методу
        :param request: user, name?, description?, is_public?, images?,
        :param args:
        :param kwargs: album_id
        :return: Album | Http404
        """

        # TODO: ако се мења име албума, треба и на диску да се промени
        album_id = self.kwargs.get('album_id',None)
        album = None

        album       = get_object_or_404(Album, pk=album_id)
        name        = request.POST.get('name', album.name)
        description = request.POST.get('description', album.description)
        images      = request.FILES.getlist('images')
        is_public   = request.POST.get('is_public', album.is_public)
        owner_id    = request.POST.get('owner', album.profile_set.get().id)
        owner = None

        # корени директоријум за све албуме
        album_root = MEDIA_ROOT + "/img/"
        # стара путања до албума
        old_album_path = prepare_path(album_root + album.name)
        # нова путања до албума
        new_album_path = prepare_path(album_root + name)

        log(f"Old album path: {old_album_path}\nNew album path: {new_album_path}")

        # ако је име албума промењено, промени и име директоријума албума
        if album.name != name:
            if os.path.exists(old_album_path):
                log("Exist!")
                os.rename(old_album_path, new_album_path)
            else:
                log("Does not exist!")

        album.name        = name if name else album.name
        album.description = description if description else album.description
        album.is_public   = is_public if is_public is not None else album.is_public
        album.set_owner(owner if owner is not None else album.owner)

        if images:
            try:
                for img in images:
                    print(img)
                    image_full = {'name': img.name, 'image': img, 'is_public': True, 'album_id': album.id}
                    image = Image.objects.create(
                        name      = image_full['name'],
                        album_id  = image_full['album_id'],
                        is_public = image_full['is_public'],
                        image     = image_full['image']
                    )
                    image.save()
                    album.images.add(image)
            except Exception as e:
                log(f"Error: {str(e)}")

        album.save()
        serializer = DetailedAlbumSerializer(instance=album)
        return JsonResponse(serializer.data)


    def delete(self, request, *args, **kwargs):
        """
        Метода која се користи за брисање инстанце
        Окида се на HTTP DELETE методу
        :param request: user
        :param args:
        :param kwargs: album_id
        :return: JsonResponse
        """
        import shutil

        album_id = self.kwargs.get('album_id', None)

        album = get_object_or_404(Album, pk=album_id)
        name  = prepare_path(album.name)
        try:
            # брисање директоријума албума
            shutil.rmtree(MEDIA_ROOT + "/img/" + name + "/")
        except Exception as e:
            log("Error while removing album files: " + str(e))

        # брисање свих асоцијација слике и албума
        images = album.images.all().delete()
        for img in images:
            img.delete()

        try:
            album.delete()
            return JsonResponse({"status": "success", "code": 200, "data": None,
                                 "messages": ["Album is successfully deleted!"]})
        except:
            return JsonResponse(
                {"status": "fail", "code": 500, "data": None, "messages": ["Error: Album was not deleted!"]})


