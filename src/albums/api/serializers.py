from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from src.albums.models import Album
from src.images.models import Image
from src.profiles.api.serializers import UserSerializer
from src.profiles.api.serializers import ProfileSerializer

from src.images.api.serializers import DetailedImageSerializer


class AlbumSerializer(ModelSerializer):
    """

    """
    owner = SerializerMethodField()

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

    def get_owner(self, obj):
        return ProfileSerializer(instance=obj.owner).data['id']


class DetailedAlbumSerializer(ModelSerializer):
    """

    """

    owner = SerializerMethodField()
    images = SerializerMethodField()

    class Meta:
        model = Album
        fields = [
            'id',
            'name',
            'description',
            'owner',
            'images',
            'is_public',
            'timestamp',
            'updated'
        ]

    def get_images(self, obj):
        from src.images.api.serializers import ImageSerializer
        return ImageSerializer(Image.objects.filter(album_id=obj.id), many=True).data

    def get_owner(self,obj):
        from src.profiles.api.serializers import ProfileSerializer
        return ProfileSerializer(instance=obj.owner).data

class CreateAlbumSerializer(ModelSerializer):
    """

    """

    class Meta:
        model = Album

        # owner = SerializerMethodField()

        fields = [
            'id',
            # 'owner',
            'name',
            'description',
            'images',
            'is_public',
        ]

        # def get_owner(self, obj):
        #     from src.profiles.api.serializers import ProfileSerializer
        #     return ProfileSerializer(instance=obj.owner).data
