import ipdb
from rest_framework.permissions import BasePermission, SAFE_METHODS
from src.albums.models import Album
from src.gallery.helpers import log


class IsOwnerOrReadOnly(BasePermission):
    """
    Класа права приступа која пропушта само власника да мења стање објекта.
    Ако није власник може само да добије информације о објекту.
    """
    message = "Морате бити власник да бисте могли мењати информације."

    # Ако има право приступа објекту
    def has_object_permission(self, request, view, obj):
        album = Album.objects.get(pk=obj.album.id) # добављање једног објекта по параметру
        owner = album.owner

        if not owner:
            return False

        log(f"request user is: {str(request.user)} and obj user is: {str(owner)}")
        if request.method in SAFE_METHODS:
            # ако је пријављени корисник власник
            return owner == request.user
        else:
            print("Not in safe methods")


class IsAdminOrOwnerOrReadOnly(BasePermission):
    """
    Класа права приступа која пропушта само власника
    или супер корисника да мења стање објекта.
    Ако није власник или корисник може само да
    добије информације о објекту.
    """
    message = "Морате бити админ или власник да бисте могли мењати ове информације."

    # Ако има право приступа објекту
    def has_object_permission(self, request, view, obj):
        image_owner = obj.album.owner
        if not image_owner:
            return False

        log(image_owner)
        # ако је аутентификовани корисник власник или ако је аутент. корисник супер корисник, може мењати
        return image_owner.user == request.user or (request.user.is_authenticated and request.user.is_superuser)
