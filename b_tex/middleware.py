from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if '/admin/' in str(request.path) and request.path != '/admin/login':
            if not request.user.is_superuser:
                return redirect('/admin/login')

        if request.path == '/':
            return redirect('/admin/')
