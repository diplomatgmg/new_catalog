from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.http import QueryDict
from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.user.forms import UserLoginForm, UserRegisterForm
from apps.user.models import User
from mixins.mixins import CreateViewMixin, TemplateViewMixin


class UserLoginView(LoginView):
    template_name = "user/login.html"
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid() and form.errors.get("username"):
            user = User.find_user(
                form.cleaned_data["username_or_email"],
                form.cleaned_data["password"],
            )
            if user:
                auth.login(self.request, user)
                return redirect(self.request.GET.get("next", self.request.path))
            messages.error(request, "Неверное имя пользователя и/или пароль")
        return self.form_invalid(form)


class UserRegisterView(CreateViewMixin, TemplateViewMixin):
    template_name = "user/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("index:index")

    def form_valid(self, form):
        form.save()
        username, password = (
            form.cleaned_data["username"],
            form.cleaned_data["password1"],
        )
        user = auth.authenticate(username=username, password=password)
        auth.login(self.request, user)
        return redirect(self.request.GET.get("next", self.request.path))
