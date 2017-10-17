from rest_framework.permissions import BasePermission, SAFE_METHODS
from src.gallery.helpers import log


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
        like_owner = obj.owner # добављање инстанце аутора лајка
        if not like_owner:
            return False
        log(like_owner)
        # ако је аутент. корисник власник или суперкорисник
        return like_owner.user == request.user or request.user.is_superuser
