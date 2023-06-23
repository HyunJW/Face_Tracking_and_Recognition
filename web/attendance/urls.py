from django.urls import path
from .views import (
    home,
    start,
    UserLoginView,
    AdminLoginView,
    UserSignUpView,
    AdminSignUpView,
    UserLogoutView,
    AdminLogoutView,
)

app_name = 'attendance'

urlpatterns = [
    path('', home, name='home'),
    path('start/', start, name='start'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('signup/', UserSignUpView.as_view(), name='user_signup'),
    path('admin/signup/', AdminSignUpView.as_view(), name='admin_signup'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('admin/logout/', AdminLogoutView.as_view(), name='admin_logout'),
]
