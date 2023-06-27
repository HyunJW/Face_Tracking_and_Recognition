from django.urls import path
from user.views import (
    UserRegistrationView,
    UserLoginView,
    user_info
)
from django.contrib.auth.views import LogoutView
from attendance.views import user_class

app_name = 'user'

urlpatterns = [
    path('create/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('info/', user_info),
    path('class/', user_class),
]
