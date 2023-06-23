from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from .forms import UserRegistrationForm

User = get_user_model()


def home(request):
    if not request.user.is_authenticated:
        return redirect('start')
    elif request.user.is_staff:
        return render(request, 'attendance/admin.html')
    else:
        return render(request, 'attendance/main.html')


def start(request):
    return render(request, 'attendance/start.html')


class UserLoginView(LoginView):
    template_name = 'attendance/user_login.html'
    redirect_authenticated_user = True


class AdminLoginView(LoginView):
    template_name = 'attendance/admin_login.html'
    redirect_authenticated_user = True


class UserSignUpView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = '/login'


class AdminSignUpView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = '/admin/login'


class UserLogoutView(LogoutView):
    next_page = '/'


class AdminLogoutView(LogoutView):
    next_page = '/'
