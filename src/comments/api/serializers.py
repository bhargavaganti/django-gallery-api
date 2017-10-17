from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.comments.models import Comment

from src.images.models import Image
from src.profiles.api.serializers import ProfileSerializer


class CommentSerializer(ModelSerializer):
    """
    Класа која претвара инстанцу модела класе у JSON објекат;
    Враћа само основне податке о коментару
    """

    class Meta:
        # о ком моделу је реч
        model = Comment

        # која поља ће се серијализовати
        fields = [
            'id',
            'owner',
            'image',
            'content'
        ]


class DetailedCommentSerializer(ModelSerializer):
    """
    Класа за серијализацију инстанце Коментар модела;
    Враћа све постојеће податке за модел Коментар
    """
    # Атрибути који се не налази у низу атрибута код Коментар модела
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

    # Методе која омогућава попуњавање Власник атрибута који је наведен горе
    def get_image(self, obj):
        from src.images.api.serializers import ImageSerializer
        return ImageSerializer(Image.objects.get(pk=obj.image.get().id)).data

    def get_owner(self, obj):
        from src.profiles.api.serializers import ProfileSerializer
        from src.profiles.models import Profile
        return ProfileSerializer(Profile.objects.get(pk=obj.owner.first().id)).data


class CreateCommentSerializer(ModelSerializer):
    """
    Класа за серијализацију инстанце Коментар модела;
    Серијализује JSON објекат у инстанцу модела Коментар

    """

    class Meta:
        model = Comment

        fields = [
            'owner',
            'image',
            'content',
        ]

