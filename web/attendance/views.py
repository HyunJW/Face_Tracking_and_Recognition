from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import AttendanceDaily, UserList, ClassTime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import json
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


def start(request):
    return redirect(home)


@csrf_exempt
def home(request):
    user = request.user
    userlist = UserList.objects.filter(student_id=user.id)
    if userlist:
        class_id = userlist[0].class_id.id
        classtime = ClassTime.objects.filter(class_id_id=class_id)[0]
        idx = datetime.today().weekday()
        if idx == 0:
            start_time, end_time = classtime.mon_start, classtime.mon_end
        elif idx == 1:
            start_time, end_time = classtime.tue_start, classtime.tue_end
        elif idx == 2:
            start_time, end_time = classtime.wed_start, classtime.wed_end
        elif idx == 3:
            start_time, end_time = classtime.thu_start, classtime.thu_end
        elif idx == 4:
            start_time, end_time = classtime.fri_start, classtime.fri_end
        elif idx == 5:
            start_time, end_time = classtime.sat_start, classtime.sat_end
        elif idx == 6:
            start_time, end_time = classtime.sun_start, classtime.sun_end

    else:
        start_time, end_time = None, None

    return render(request, 'attendance/home.html', {'userlist': userlist, 'start_time': start_time, 'end_time': end_time})


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
