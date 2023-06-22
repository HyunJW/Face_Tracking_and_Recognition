from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import CustomUserCreationForm, CustomAdminUserCreationForm
import hashlib


def home(request):
    if not request.user.is_authenticated:
        return redirect('start')
    elif request.user.is_staff:
        return render(request, 'attendance/admin.html')
    else:
        return render(request, 'attendance/main.html')


def start(request):
    return render(request, 'attendance/start.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password = hashlib.sha256(password.encode()).hexdigest()

        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            auth_login(request, user)
            return render(request, 'attendance/main.html')
        else:
            return render(request, 'attendance/user_login.html', {'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'})
    else:
        return render(request, 'attendance/user_login.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password = hashlib.sha256(password.encode()).hexdigest()

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            auth_login(request, user)
            return render(request, 'attendance/admin.html')
        else:
            return render(request, 'attendance/admin_login.html',
                          {'msg': '아이디 또는 비밀번호가 일치하지 않거나 권한이 없습니다.'})
    else:
        return render(request, 'attendance/admin_login.html')


def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_signup.html', {'form': form})


def admin_signup(request):
    if request.method == 'POST':
        form = CustomAdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_login')
    else:
        form = CustomAdminUserCreationForm()
    return render(request, 'admin_signup.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('/')
