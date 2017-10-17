from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.albums.models import Album
from src.images.models import Image
from src.profiles.api.serializers import UserSerializer
from src.profiles.api.serializers import ProfileSerializer

from src.images.api.serializers import DetailedImageSerializer


class AlbumSerializer(ModelSerializer):
    """
    Класа која претвара инстанцу модела класе у JSON објекат;
    Враћа само основне податке о албуму
    """
    # Атрибут који се не налази у низу атрибута код Албум модела, а асоцијативни су са албумом
    owner = SerializerMethodField()

    class Meta:
        # о ком моделу је реч
        model = Album

        # која поља ће се серијализовати
        fields = [
            'id',
            'owner',
            'name',
            'description',
            'images',
            'is_public',
        ]

    # Метода која омогућава попуњавање Власник атрибута који је наведен горе
    def get_owner(self, obj):
        return ProfileSerializer(instance=obj.profile_set.first()).data


class DetailedAlbumSerializer(ModelSerializer):
    """
    Класа за серијализацију инстанце Албум модела;
    Враћа све постојеће податке за модел Албум
    """

    owner = SerializerMethodField()
    images = SerializerMethodField()

    class Meta:
        model = Album
        fields = [
            'id',
            'name',
            'description',
            'owner',
            'images',
            'is_public',
            'timestamp',
            'updated'
        ]

    def get_images(self, obj):
        from src.images.api.serializers import ImageSerializer
        return ImageSerializer(Image.objects.filter(album_id=obj.id), many=True).data

    def get_owner(self,obj):
        from src.profiles.api.serializers import ProfileSerializer
        return ProfileSerializer(instance=obj.profile_set.get()).data


class CreateAlbumSerializer(ModelSerializer):
    """
    Класа за серијализацију инстанце Албум модела;
    Серијализује JSON објекат у инстанцу модела Албум

    """

    class Meta:
        model = Album

        fields = [
            'id',
            'name',
            'description',
            'images',
            'is_public',
        ]
