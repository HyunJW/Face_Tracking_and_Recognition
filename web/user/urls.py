from django.urls import path
from user.views import (
    UserRegistrationView,
    UserLoginView,
    # AdminLoginView,
)
from django.contrib.auth.views import LogoutView

app_name = 'user'

urlpatterns = [
    path('create/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('user/logout/', LogoutView.as_view()),
    # path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
]
