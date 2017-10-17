from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.images.models import Image

from src.comments.api.serializers import CommentSerializer
from src.likes.api.serializers import LikeSerializer


class ImageSerializer(ModelSerializer):
    """
    Класа која претвара инстанцу модела класе у JSON објекат;
    Враћа само основне податке о слици
    """

    class Meta:
        # о ком моделу је реч
        model = Image

        # која поља ће се серијализовати
        fields = [
            'id',
            'name',
            'description',
            'album',
            'image',
            'is_public',
        ]
    # за поље image, враћа само њену локацију
    def get_image(self, obj):
        return obj.image.url


class DetailedImageSerializer(ModelSerializer):
    """
    Класа за серијализацију инстанце модела Слике;
    Враћа све постојеће податке за модел Слика
    """

    # Атрибути који се не налазе у низу атрибута код Албум модела,а асоцијативни су са сликом
    comments = SerializerMethodField()
    likes    = SerializerMethodField()
    tags     = SerializerMethodField()

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

        comments_qs = obj.comment_set.all()
        return CommentSerializer(comments_qs, many=True).data

    def get_likes(self, obj):
        from src.likes.api.serializers import LikeSerializer
        from src.likes.models import Like

        comments_qs = obj.like_set.all()
        return LikeSerializer(comments_qs, many=True).data

    def get_tags(self, obj):
        from src.tags.api.serializers import TagSerializer
        tags_qs = obj.tag_set.all()
        return TagSerializer(tags_qs, many=True).data


class CreateImageSerializer(ModelSerializer):
    """
    Класа за серијализацију инстанце модела Слика;
    Серијализује JSON објекат у инстанцу модела Слика
    """

    class Meta:
        model = Image
        fields = [
            'album',
            'image',
            'name',
            'description',
            'is_public',
        ]

