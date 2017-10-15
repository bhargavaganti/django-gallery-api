from rest_framework.permissions import BasePermission, SAFE_METHODS
from src.profiles.models import Profile


class IsOwnerOrReadOnly(BasePermission):
    """

    """
    message = "Морате бити власник да бисте могли мењати информације."
    my_safe_methods = ['GET', 'PUT']

    # Ако има право присутпа крајњој тачки (end-point-у)
    def has_permission(self, request, view):
        # print(f"Built-in safe methods: {SAFE_METHODS}")
        if request.method in self.my_safe_methods:
            return True
        return False

    # Ако има право приступа објекту
    def has_object_permission(self, request, view, obj):
        user = obj.user

        if request.method in SAFE_METHODS:
            return True
        # print(f"request user is: {str(request.user)} and obj user is: {str(user)}")
        return user == request.user


class IsAdminOrOwnerOrReadOnly(BasePermission):
    """

    """
    message = "Морате бити власник да бисте могли мењати информације."
    my_safe_methods = ['GET', 'PUT', 'POST', 'DELETE']

    # # Ако има право присутпа крајњој тачки (end-point-у)
    # def has_permission(self, request, view):
    #     if request.method in self.my_safe_methods:
    #         #    print("Метода је: ", request.method)
    #         return True
    #     # print("Метода није у ", self.my_safe_methods)
    #     return False

    # Ако има право приступа објекту
    def has_object_permission(self, request, view, obj):
        user = obj.user

        # print(f"request user is: {str(request.user)} and obj user is: {str(user)}")
        if request.method in SAFE_METHODS:
            return user == request.user or request.user.is_superuser

