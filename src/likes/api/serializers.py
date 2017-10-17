import ipdb
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.likes.models import Like
from src.images.models import Image
from src.profiles.api.serializers import ProfileSerializer



class LikeSerializer(ModelSerializer):
    """
    Класа која претвара инстанцу модела класе у JSON објекат;
    Враћа само основне податке о лајку
    """

    class Meta:
        # о ком моделу је реч
        model = Like

        # која поља ће се серијализовати
        fields = [
            'id',
            'owner',
            'image',
            'timestamp',
        ]


class DetailedLikeSerializer(ModelSerializer):
    """
    Класа за серијализацију инстанце модела Лајк;
    Враћа све постојеће податке за модел Лајк
    """

    # Атрибути који се не налазе у низу атрибута код Лајк модела,а асоцијативни су са сликом
    image = SerializerMethodField()
    owner = SerializerMethodField()

    class Meta:
        model = Like
        fields = [
            'id',
            'owner',
            'image',
            'timestamp',
            'updated'
        ]

    # Серијализација поља којих нема непосредно у моделу Лајк

    def get_image(self, obj):
        from src.images.api.serializers import ImageSerializer

        return ImageSerializer(Image.objects.get(pk=obj.image.get().id)).data

    def get_owner(self, obj):
        from src.profiles.api.serializers import ProfileSerializer
        from src.profiles.models import Profile

        return ProfileSerializer(Profile.objects.get(pk=obj.owner.get().id)).data


class CreateLikeSerializer(ModelSerializer):
    """
    Класа за серијализацију инстанце модела Лајк;
    Серијализује JSON објекат у инстанцу модела Лајк
    """
    class Meta:
        model = Like
        fields = [
            'owner',
            'image',
        ]


