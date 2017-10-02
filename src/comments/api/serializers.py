from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.comments.models import Comment

from src.images.api.serializers import ImageSerializer
from src.images.models import Image
from src.profiles.api.serializers import ProfileSerializer


class CommentSerializer(ModelSerializer):
    """

    """
    image = SerializerMethodField()
    owner = ProfileSerializer()

    # image = SerializerMethodField() # TODO: image серијализатор ће бити имплементиран у својој класи

    class Meta:
        model = Comment
        fields = [
            'id',
            'owner',
            'image',
            'content',
            'timestamp',
            'updated'
        ]

    def get_image(self, obj):
        images_qs = Image.objects.get(pk=obj.image.id)
        images = ImageSerializer(images_qs).data
        return images


class CreateCommentSerializer(ModelSerializer):
    """

    """
    # image = SerializerMethodField()
    # owner = ProfileSerializer()

    class Meta:
        model = Comment
        fields = [
            'owner',
            'image',
            'content',
            'timestamp',
        ]

    # def get_image(self, obj):
    #     return obj.image.id
