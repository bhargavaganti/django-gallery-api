from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.images.models import Image

from src.comments.api.serializers import CommentSerializer
from src.likes.api.serializers import LikeSerializer


class ImageSerializer(ModelSerializer):
    """

    """

    class Meta:
        model = Image
        fields = [
            'id',
            'name',
            'description',
            'album',
            'image',
            # 'tags',
            # 'comments',
            # 'likes',
            'is_public',
            'timestamp',
            'updated'
        ]

    def get_image(self, obj):
        return obj.image.url


class DetailedImageSerializer(ModelSerializer):
    """

    """

    comments = SerializerMethodField()
    likes = SerializerMethodField()
    # tags = SerializerMethodField()

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
        from src.comments.models import Comment

        comments_qs = Comment.objects.filter(image__pk=obj.id)
        return CommentSerializer(comments_qs, many=True).data

    def get_likes(self, obj):
        from src.likes.api.serializers import LikeSerializer
        from src.likes.models import Like

        comments_qs = Like.objects.filter(image__pk=obj.id)
        return LikeSerializer(comments_qs, many=True).data

    # def get_tags(self, obj):
    #     from src.tags.api.serializers import TagSerializer
    #     return TagSerializer(obj.tags.all(), many=True).data


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
