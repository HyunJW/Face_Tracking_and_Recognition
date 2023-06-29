from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import AttendanceDaily
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import json
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


def start(request):
    return redirect(home)


@csrf_exempt
def home(request):
    date = datetime.now().date()
    selected_log = AttendanceDaily.objects.filter(date=date)
    user = request.user
    attendances = selected_log.filter(user_id=user.id)

    return render(request, 'attendance/home.html', {'attendances': attendances})


def user_class(request):
    return render(request, 'user/class.html')


@login_required
@csrf_exempt
def home_selected(request):
    data = json.loads(request.body)
    selected_date = data.get('selectedDate')
    selected_date = selected_date.split('T')[0]
    selected_log = AttendanceDaily.objects.filter(date=selected_date)
    user = request.user
    attendances = selected_log.filter(user_id=user.id)

    return render(request, 'attendance/table1.html', {'attendances': attendances})