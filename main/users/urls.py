from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import SignIn, SignUp

urlpatterns = [
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path(
        'logout/', LogoutView.as_view(next_page='sign-in'),
        name='logout'
    ),
]