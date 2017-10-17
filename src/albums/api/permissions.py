import ipdb
from rest_framework.permissions import BasePermission, SAFE_METHODS
from src.gallery.helpers import log


class IsOwnerOrReadOnly(BasePermission):
    """
    Класа права приступа која пропушта само власника да мења стање објекта.
    Ако није власник може само да добије информације о објекту.
    """
    message = "Морате бити власник да бисте могли мењати информације."
    my_safe_methods = ['GET', 'POST', 'PUT', 'DELETE']

    # Ако има право присутпа крајњој тачки (end-point-у)
    def has_permission(self, request, view):
        if request.method in self.my_safe_methods:
            return True
        return False

    # Ако има право приступа самом објекту
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # ако је пријављени корисник власник
        return obj.owner.get().user == request.user


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
        album_owner = obj.owner
        if not album_owner:
            return False
        # ако је аутентификовани корисник власник или ако је аутент. корисник супер корисник, може мењати
        return album_owner.user == request.user or (request.user.is_authenticated and request.user.is_superuser)
