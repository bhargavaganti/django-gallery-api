from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.albums.models import Album

class AlbumSerializer(ModelSerializer):
    """

    """
    owner = SerializerMethodField()
    image = SerializerMethodField() # TODO: image серијализатор ће бити имплементиран у својој класи

    class Meta:
        model = Album
        fields = [
            'id',
            'owner',
            'name',
            'description',
            'images',
            'is_public',
            'timestamp',
            'updated'
        ]

class CreateAlbumSerializer(ModelSerializer):
    """

    """
    class Meta:
        model = Album
        fields = [
            'owner',
            'name',
            'description',
            'images',
            'is_public',
        ]