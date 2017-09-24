from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """

    """
    message = "Морате бити власник да бисте могли мењати информације."
    my_safe_methods = ['GET', 'PUT']

    # Ако има право присутпа крајњој тачки (end-point-у)
    def has_permission(self, request, view):
        print(f"Built-in safe methods: {SAFE_METHODS}")
        if request.method in self.my_safe_methods:
            return True
        return False

    # Ако има право приступа објекту
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        print(f"request user is: {str(request.user)} and obj user is: {str(obj.owner.user)}")
        return obj.owner.user == request.user
