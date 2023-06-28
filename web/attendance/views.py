from django.shortcuts import render, redirect
from .models import AttendanceDaily
from django.contrib.auth.decorators import login_required


def start(request):
    return redirect(home)


def home(request):
    return render(request, 'attendance/home.html')


def user_class(request):
    return render(request, 'user/class.html')

@login_required
def daily_log(request):
    user = request.user
    attendances = AttendanceDaily.objects.filter(user_id=user)

    return render(request, 'attendance/home.html',{'attendances': attendances})