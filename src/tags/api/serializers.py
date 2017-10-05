from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.tags.models import Tag

from src.images.api.serializers import ImageSerializer, DetailedImageSerializer
from src.images.models import Image


class TagSerializer(ModelSerializer):
    """

    """

    # images = SerializerMethodField()

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            # 'images',
            'timestamp',
            'updated'
        ]

        # def get_images(self, obj):
        #     images_qs = Image.objects.all()
        #     images = ImageSerializer(images_qs, many=True).data
        #     return images


class DetailedTagSerializer(ModelSerializer):
    """

    """
    images = SerializerMethodField()

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
