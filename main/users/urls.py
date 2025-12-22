from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import SignIn, SignUp, my_profile_page

urlpatterns = [
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path(
        'logout/', LogoutView.as_view(next_page='sign-in'),
        name='logout'
    ),
    #path('profile/<slug:slug>/', name='profile'),
    path(
        'profile-settings/<slug:slug>/', my_profile_page,
        name='profile-settings'
    ),
]