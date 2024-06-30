from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
  """
    Custom permission to only allow administrators to edit objects.

    Methods:
    - has_permission (function): Grants permission if the request
      method is safe (e.g., GET, HEAD, OPTIONS) or if the user is
      an administrator.
    """
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    return bool(request.user and request.user.is_staff)

class FullPermissions(permissions.DjangoModelPermissions):
  """
    Custom permissions class to add full permissions for GET requests.

    Attributes:
    - perms_map (dict): Maps HTTP methods to required permissions.
    
    Methods:
    - __init__ (function): Initializes the permission map for GET requests.
    """
  def __init__(self) -> None:
    self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']