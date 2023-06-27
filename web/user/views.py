from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from user.forms import UserRegistrationForm, LoginForm
from django.contrib import messages

User = get_user_model()


def start():
    return redirect(home)


def home(request):
    return render(request, 'user/home.html')


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = '/home/'


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'user/login_form.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)
