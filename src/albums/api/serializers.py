from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.albums.models import Album
from src.images.models import Image

from src.profiles.api.serializers import UserSerializer

from src.profiles.api.serializers import ProfileSerializer


class AlbumSerializer(ModelSerializer):
    """

    """
    owner = ProfileSerializer()
    # images = SerializerMethodField() # TODO: image серијализатор ће бити имплементиран у својој класи

    class Meta:
        model = Album
        fields = [
            'id',
            'owner',
            'name',
            'description',
            'images',
            'is_public',
            'timestamp',
            'updated'
        ]


    # def get_images(self, obj):
    #     return Image.objects.filter(album=obj)
    #
class CreateAlbumSerializer(ModelSerializer):
    """

    """
    class Meta:
        model = Album
        fields = [
            'id',
            'owner',
            'name',
            'description',
            'images',
            'is_public',
        ]