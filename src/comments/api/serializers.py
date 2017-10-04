from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.comments.models import Comment

from src.images.models import Image
from src.profiles.api.serializers import ProfileSerializer


class CommentSerializer(ModelSerializer):
    """

    """

    # image = SerializerMethodField()
    # owner = ProfileSerializer()

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
        #
        # def get_image(self, obj):
        #     images_qs = Image.objects.get(pk=obj.image.id)
        #     images = ImageSerializer(images_qs).data
        #     return images


class DetailedCommentSerializer(ModelSerializer):
    """

    """
    image = SerializerMethodField()
    # owner = SerializerMethodField()
    # owner = ProfileSerializer()

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

    #
    def get_image(self, obj):
        from src.images.api.serializers import ImageSerializer
        images_qs = obj.image.get()
        images = ImageSerializer(images_qs).data
        return images

    # def get_owner(self, obj):
    #     return ProfileSerializer(obj.owner.all()).data


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
