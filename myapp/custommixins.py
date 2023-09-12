from rest_framework.exceptions import PermissionDenied

class LibrarianRequiredMixin:
    """
    Mixin to restrict access to librarians.
    """
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.user_type == 'librarian':
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to access this page.")

class StudentRequiredMixin:
    """
    Mixin to restrict access to students.
    """
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.user_type == 'student':
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to access this page.")
