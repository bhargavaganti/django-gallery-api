from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.images.models import Image

from src.albums.api.serializers import AlbumSerializer


class ImageSerializer(ModelSerializer):
    """

    """
    image = SerializerMethodField()

    class Meta:
        model = Image
        fields = [
            'id',
            'name',
            'description',
            'album',
            'image',
            'tags',
            'is_public',
            'timestamp',
            'updated'
        ]

    def get_image(self, obj):
        return obj.image.url


class CreateImageSerializer(ModelSerializer):
    """

    """
    # album = AlbumSerializer()
    # album = SerializerMethodField()

    class Meta:
        model = Image
        fields = [
            'album',
            'image',
            'name',
            'description',
            'is_public',
            'tags'
        ]


