from rest_framework.permissions import BasePermission, SAFE_METHODS
from src.gallery.helpers import log


class IsAdminOrOwnerOrReadOnly(BasePermission):
    """
    Класа права приступа која пропушта само власника
    или супер корисникада мења стање објекта.
    Ако није власник или корисник
    може само да добије информације о објекту.
    """
    message = "Морате бити админ или власник да бисте могли мењати ове информације."

    # Ако има право приступа објекту
    def has_object_permission(self, request, view, obj):
        comment_owner = obj.owner # добављање једног објекта по параметру
        if not comment_owner:
            return False
        # ако је аутентификовани корисник власник или ако је аутент. корисник супер корисник
        return comment_owner.user == request.user or request.user.is_superuser
