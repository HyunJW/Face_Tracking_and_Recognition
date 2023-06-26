from django.urls import path
from user.views import (
    UserRegistrationView,
    UserLoginView,
)
from django.contrib.auth.views import LogoutView

app_name = 'user'

urlpatterns = [
    path('create/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
