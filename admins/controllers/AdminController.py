from typing import Any
from admins.forms import UserForm
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView, CreateView
from django.shortcuts import redirect
from django.db.models import Q
from core.services import ModelViewService


# super users list
class AdminsList(ListView):
    model = User
    template_name = 'admin/moterators_list.html'

    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=True)
        query = self.request.GET.get("q", '')

        if query != '':
            queryset = queryset.filter(Q(username__iregex=query) | Q(
                first_name__iregex=query) | Q(last_name__iregex=query))

        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super(AdminsList, self).get_context_data(**kwargs)

        view_service = ModelViewService(User)

        self.queryset = self.get_queryset()

        assert self.queryset != None

        user_context = view_service.get_list_context_data(
            self.request, self.queryset)

        context.update(user_context)

        return context


# super user create
class AdminCreate(CreateView):
    model = User
    form_class = UserForm
    success_url = '/'
    template_name = 'admin/moder_form.html'

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_superuser = True
        full_name = self.request.POST.get("name")

        if full_name:
            full_name = full_name.split(' ')
            if len(full_name) > 0:
                new_user.first_name = full_name[0]

            if len(full_name) == 2:
                new_user.last_name = full_name[1]

        new_user.save()

        return redirect('admin_list')


# admin udate
class AdminUpdate(UpdateView):
    model = User
    form_class = UserForm
    success_url = '/'
    template_name = 'admin/moder_form.html'

    def get_context_data(self, **kwargs):
        context = super(AdminUpdate, self).get_context_data(**kwargs)
        context['full_name'] = ""

        self.object: Any = self.get_object()

        if self.object.first_name:
            context['full_name'] = self.object.first_name + " "

        if self.object.last_name:
            context['full_name'] += self.object.last_name

        return context

    def form_valid(self, form):
        user = form.save()
        user.is_superuser = True
        full_name = self.request.POST.get("name")

        if full_name:
            if len(full_name.split(' ')) > 0:
                user.first_name = full_name.split(' ')[0]

            if len(full_name.split(' ')) == 2:
                user.last_name = full_name.split(' ')[1]

        user.save()

        return redirect('admin_list')
