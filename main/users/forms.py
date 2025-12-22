from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django.forms.widgets import TimeInput

from users.models import Profile, WorkingDays


class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username', 'first_name', 'last_name', 'email',
        ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio', 'address', 'phone_number'
        ]


class ProviderStatusUpdate(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['is_provider']


WorkingDaysSet = inlineformset_factory(
    Profile,
    WorkingDays,
    fields=['is_day_off', 'start_time', 'end_time'],
    extra=0,
    can_delete=False,
    widgets={
        'start_time': TimeInput(format='%H:%M', attrs={'type': 'time'}),
        'end_time': TimeInput(format='%H:%M', attrs={'type': 'time'})
    }
)