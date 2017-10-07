from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """

    """
    message = "Морате бити власник да бисте могли мењати информације."
    my_safe_methods = ['GET', 'POST', 'PUT', 'DELETE']

    # Ако има право присутпа крајњој тачки (end-point-у)
    def has_permission(self, request, view):
        if request.method in self.my_safe_methods:
            return True
        return False

    # Ако има право приступа објекту
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        print(f"request user is: {str(request.user)} and obj user is: {str(obj.owner.get().user)}")
        return obj.owner.get().user == request.user
