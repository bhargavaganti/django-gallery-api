from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.comments.models import Comment

from src.images.models import Image
from src.profiles.api.serializers import ProfileSerializer


class CommentSerializer(ModelSerializer):
    """

    """

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


class DetailedCommentSerializer(ModelSerializer):
    """

    """
    image = SerializerMethodField()
    owner = SerializerMethodField()

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
        return ImageSerializer(Image.objects.get(pk=obj.image.get().id)).data

    def get_owner(self, obj):
        from src.profiles.api.serializers import ProfileSerializer
        from src.profiles.models import Profile
        return ProfileSerializer(Profile.objects.get(pk=obj.owner.get().id)).data


class CreateCommentSerializer(ModelSerializer):
    """

    """

    class Meta:
        model = Comment
        fields = [
            'owner',
            'image',
            'content',
        ]

