from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.images.models import Image

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
    class Meta:
        model = Image
        fields = [
            'image',
            'name',
            'description',
            'is_public',
            'tags'
        ]