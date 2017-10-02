from rest_framework.permissions import BasePermission, SAFE_METHODS
from src.albums.models import Album

class IsOwnerOrReadOnly(BasePermission):
    """

    """
    message = "Морате бити власник да бисте могли мењати информације."
    my_safe_methods = ['GET', 'PUT']

    # Ако има право присутпа крајњој тачки (end-point-у)
    # def has_permission(self, request, view):
    #    pass

    # Ако има право приступа објекту
    def has_object_permission(self, request, view, obj):
        album_owner = Album.objects.get(pk=obj.album_id) # добављање једног објекта по параметру
        owner = album_owner.owner.user

        if request.method in SAFE_METHODS:
            return True
        print(f"request user is: {str(request.user)} and obj user is: {str(owner)}")
        return owner == request.user or request.user.is_superuser
