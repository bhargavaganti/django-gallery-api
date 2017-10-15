import ipdb
from rest_framework.permissions import BasePermission, SAFE_METHODS
from src.albums.models import Album
from src.gallery.helpers import log


class IsOwnerOrReadOnly(BasePermission):
    """

    """
    message = "Морате бити власник да бисте могли мењати информације."

    # Ако има право приступа објекту
    def has_object_permission(self, request, view, obj):
        album_owner = Album.objects.get(pk=obj.album.pk) # добављање једног објекта по параметру
        if not album_owner:
            return False
        owner = album_owner.owner.user

        log(album_owner)

        print(f"request user is: {str(request.user)} and obj user is: {str(owner)}")
        if request.method in SAFE_METHODS:
            return owner == request.user or request.user.is_superuser
        else:
            print("Not in safe methods")

class IsAdminOrOwnerOrReadOnly(BasePermission):
    """

    """
    message = "Морате бити админ или власник да бисте могли мењати ове информације."

    # Ако има право приступа објекту
    def has_object_permission(self, request, view, obj):
        image_owner = obj.album.owner # добављање једног објекта по параметру
        if not image_owner:
            return False

        log(image_owner)

        if request.method in SAFE_METHODS:
            return image_owner.user == request.user or request.user.is_superuser
        else:
            print("Not in safe methods")