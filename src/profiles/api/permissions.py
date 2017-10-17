from rest_framework.permissions import BasePermission, SAFE_METHODS
from src.profiles.models import Profile


class IsOwnerOrReadOnly(BasePermission):
    """
    Класа права приступа која пропушта само власника да мења стање објекта.
    Ако није власник може само да добије информације о објекту.

    """
    message = "Морате бити власник да бисте могли мењати информације."

    # Ако има право приступа објекту
    def has_object_permission(self, request, view, obj):
        user = obj.user

        print(f"request user is: {str(request.user)} and obj user is: {str(user)}")
        # ако је аутент. корисник власник
        return user == request.user


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
        user = obj.user

        print(f"request user is: {str(request.user)} and obj user is: {str(user)}")

        # ако је аутент. корисник власник или суперкорисник
        return user == request.user or request.user.is_superuser

