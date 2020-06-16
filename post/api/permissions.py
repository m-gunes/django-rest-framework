from rest_framework.permissions import BasePermission

class isOwnerOrSuperUser(BasePermission):
   # def has_permission(self, request, view):
   #    print('has_permission')
   #    return request.user and request.user.is_authenticated

   message = 'You must be the owner of this object'
   def has_object_permission(self, request, view, obj):
      return (obj.user == request.user) or request.user.is_superuser
      
      # Read permissions are allowed to any request,
      # so we'll always allow GET, HEAD or OPTIONS requests.
      
   