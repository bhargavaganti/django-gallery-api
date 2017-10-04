from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.images.models import Image

from src.albums.api.serializers import AlbumSerializer

from src.comments.api.serializers import CommentSerializer
from src.likes.api.serializers import LikeSerializer


class ImageSerializer(ModelSerializer):
    """

    """
    # FIXME: у albums/1/images/ нема података о лајковима и коментарима

    # image = SerializerMethodField()
    comments = SerializerMethodField()
    likes = SerializerMethodField()

    class Meta:
        model = Image
        fields = [
            'id',
            'name',
            'description',
            'album',
            'image',
            'tags',
            'comments',
            'likes',
            'is_public',
            'timestamp',
            'updated'
        ]

    def get_image(self, obj):
        return obj.image.url

    def get_comments(self, obj):
        from src.comments.api.serializers import CommentSerializer
        return CommentSerializer(obj.comments.all(), many=True).data

    def get_likes(self, obj):
        from src.likes.api.serializers import LikeSerializer
        return LikeSerializer(obj.likes.all(),many=True).data


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


