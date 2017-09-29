from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.albums.models import Album
from src.images.models import Image

class AlbumSerializer(ModelSerializer):
    """

    """
    owner = SerializerMethodField()
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

    def get_owner(self, obj):
        return str(obj.owner.user.username)

    # def get_images(self, obj):
    #     return Image.objects.filter(album=obj)
    #
class CreateAlbumSerializer(ModelSerializer):
    """

    """
    class Meta:
        model = Album
        fields = [
            'owner',
            'name',
            'description',
            'images',
            'is_public',
        ]