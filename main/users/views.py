from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from users.forms import (
    UserCreateForm, ProviderStatusUpdate,
    ProfileUpdateForm, WorkingDaysSet
)


class SignUp(CreateView):
    model = get_user_model()
    form_class = UserCreateForm
    template_name = 'users/sign-up.html'
    success_url = reverse_lazy('sign-in')


class SignIn(LoginView):
    template_name = 'users/sign-in.html'
    redirect_authenticated_user = True


@login_required
def my_profile_page(request, slug):
    user_qs = (get_user_model()
               .objects.select_related('profile')
               )
    user = get_object_or_404(user_qs, slug=slug)
    profile = user.profile

    if request.user.id != user.id:
        return HttpResponseForbidden(
            'You do not have permission to view this resource.'
        )

    provider_form = ProviderStatusUpdate(
        (request.POST
            if request.method == 'POST'
            and 'submit_provider' in request.POST
         else None),
        instance=user,
        prefix='provider_form'
    )
    profile_update_form = ProfileUpdateForm(
        (request.POST
            if request.method == 'POST'
            and 'submit_profile' in request.POST
         else None),
        instance=profile,
        prefix='profile_update_form'
    )
    working_days_formset = WorkingDaysSet(
        (request.POST
            if request.method == 'POST'
            and 'submit_working_days' in request.POST
         else None),
        instance=profile,
        prefix='working_days_formset'
    )

    if request.method == 'POST':
        if 'submit_provider' in request.POST:
            if provider_form.is_valid():
                provider_form.save()
                return redirect('profile-settings', slug)

        if 'submit_profile' in request.POST:
            if profile_update_form.is_valid():
                profile_update_form.save()
                return redirect('profile-settings', slug)

        if 'submit_working_days' in request.POST:
            if working_days_formset.is_valid():
                working_days_formset.save()
                return redirect('profile-settings', slug)

    return render(
        request, 'users/user_page.html',
        {
            'provider_form': provider_form,
            'profile_update_form': profile_update_form,
            'working_days_formset': working_days_formset
        }
    )