from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.tags.models import Tag

from src.images.api.serializers import ImageSerializer
from src.images.models import Image


class TagSerializer(ModelSerializer):
    """

    """
    images = SerializerMethodField()
    # image = SerializerMethodField() # TODO: image серијализатор ће бити имплементиран у својој класи

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'images',
            'timestamp',
            'updated'
        ]

    def get_images(self, obj):
        images_qs = Image.objects.all()
        images = ImageSerializer(images_qs, many=True).data
        return images

class CreateTagSerializer(ModelSerializer):
    """

    """
    class Meta:
        model = Tag
        fields = [
            'name',
            'images',
            'timestamp',
        ]


