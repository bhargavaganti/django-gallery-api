import ipdb
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.likes.models import Like

from src.images.models import Image

from src.profiles.api.serializers import ProfileSerializer



class LikeSerializer(ModelSerializer):
    """

    """
    # image = SerializerMethodField()
    # owner = ProfileSerializer()
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

    # def get_image(self, obj):
    #     images_qs = Image.objects.get(pk=obj.image.id)
    #     images = ImageSerializer(images_qs).data
    #     return images


class DetailedLikeSerializer(ModelSerializer):
    """

    """
    image = SerializerMethodField()
    owner = SerializerMethodField()
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
        from src.images.api.serializers import ImageSerializer
        return ImageSerializer(Image.objects.get(pk=obj.image.get().id)).data

    def get_owner(self, obj):
        from src.profiles.api.serializers import ProfileSerializer
        from src.profiles.models import Profile

        return ProfileSerializer(Profile.objects.get(pk=obj.owner.get().id)).data


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


