from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserCreateForm


class SignUp(CreateView):
    model = get_user_model()
    form_class = UserCreateForm
    template_name = 'users/sign-up.html'
    success_url = reverse_lazy('sign-in')


class SignIn(LoginView):
    template_name = 'users/sign-in.html'
    redirect_authenticated_user = True