from rest_framework.permissions import BasePermission, SAFE_METHODS
from src.gallery.helpers import log


class IsAdminOrOwnerOrReadOnly(BasePermission):
    """

    """
    message = "Морате бити админ или власник да бисте могли мењати ове информације."

    # Ако има право приступа објекту
    def has_object_permission(self, request, view, obj):
        like_owner = obj.owner # добављање једног објекта по параметру
        if not like_owner:
            return False
        log(like_owner)
        if request.method in SAFE_METHODS:
            return like_owner.user == request.user or request.user.is_superuser
        else:
            print("Not in safe methods")