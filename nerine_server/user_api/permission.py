from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = 'You must be owner of this object'
    def has_object_permission(self, request, view, obj):
        my_safe_method = ['PUT']
        if request.method is my_safe_method:
            return True
        print(obj.username)
        print(request.user)
        return str(obj.username) == str(request.user)