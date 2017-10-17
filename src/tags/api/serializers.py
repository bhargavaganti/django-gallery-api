from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.tags.models import Tag

from src.images.api.serializers import ImageSerializer, DetailedImageSerializer
from src.images.models import Image


class TagSerializer(ModelSerializer):
    """
    Класа која претвара инстанцу модела класе у JSON објекат;
    Враћа само основне податке о ознаци (тагу)
    """

    class Meta:

        # о ком моделу је реч
        model = Tag

        # која поља ће се серијализовати
        fields = [
            'id',
            'name',
        ]



class DetailedTagSerializer(ModelSerializer):
    """
    Класа за серијализацију инстанце модела Ознака;
    Враћа све постојеће податке за модел Ознака
    """

    # Атрибути који се не налазе у низу атрибута код Албум модела,а асоцијативни су са сликом
    images = SerializerMethodField()

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'images',
            'timestamp',
            'updated'
        ]

    # Серијализација поља којих нема непосредно у моделу Oзнака

    def get_images(self, obj):
        images_qs = obj.images.all()
        images = ImageSerializer(images_qs, many=True).data
        return images


class CreateTagSerializer(ModelSerializer):
    """
    Класа за серијализацију инстанце модела Ознака;
    Серијализује JSON објекат у инстанцу модела Ознака;
    """

    class Meta:
        model = Tag
        fields = ['name',]
