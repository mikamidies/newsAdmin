from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Если путь содержит /admin/ и это не страница логина
        if '/admin/' in str(request.path) and request.path != '/admin/login':
            if not request.user.is_superuser:
                return redirect('/admin/login')

        # Если это корневой URL
        if request.path == '/':
            if request.user.is_authenticated:
                return redirect('/admin/news/')  # Редирект на новости для авторизованных
            return redirect('/admin/login')  # Редирект на логин для неавторизованных

        # Если это админка без конкретного пути
        if request.path == '/admin/':
            if request.user.is_authenticated:
                return redirect('/admin/news/')  # Редирект на новости
            return redirect('/admin/login')  # Редирект на логин