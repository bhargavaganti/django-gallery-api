from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.likes.models import Like

from src.images.api.serializers import ImageSerializer
from src.images.models import Image

from src.profiles.api.serializers import ProfileSerializer


class LikeSerializer(ModelSerializer):
    """

    """
    image = SerializerMethodField()
    owner = ProfileSerializer()
    # image = SerializerMethodField() # TODO: image серијализатор ће бити имплементиран у својој класи

    class Meta:
        model = Like
        fields = [
            'id',
            'owner',
            'image',
            'timestamp',
            'updated'
        ]

    def get_image(self, obj):
        images_qs = Image.objects.get(pk=obj.image.id)
        images = ImageSerializer(images_qs).data
        return images

class CreateLikeSerializer(ModelSerializer):
    """

    """
    class Meta:
        model = Like
        fields = [
            'owner',
            'image',
            'timestamp',
        ]


