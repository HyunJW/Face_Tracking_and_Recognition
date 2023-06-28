from django.shortcuts import render, redirect


def start(request):
    return redirect(home)


def home(request):
    return render(request, 'attendance/home.html')


def user_class(request):
    return render(request, 'user/class.html')
