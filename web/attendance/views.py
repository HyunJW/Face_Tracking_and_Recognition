from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from attendance.models import Attendance, UserList, ClassTime, ClassInfo
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import cv2
import threading
from attendance.signals import camera_task_stopped
from module.FaceDetectModule import FaceDetect
from module.FaceMatchModule import FaceMatch
from itertools import groupby
import math

User = get_user_model()


class CameraBackgroundTask(threading.Thread):
    def __init__(self, camera_index):
        super(CameraBackgroundTask, self).__init__()
        self._stop_event = threading.Event()
        self.fd = FaceDetect()
        self.fm = FaceMatch()
        self.camera_index = camera_index

    def run(self):
        cap = cv2.VideoCapture(self.camera_index)  # 웹캠에 접근하기 위해 0을 사용합니다.
        # cap = cv2.VideoCapture('d:/video/enter.mp4') # 동영상 사용

        while not self._stop_event.is_set():
            ret, frame = cap.read()  # 영상 프레임을 읽어옵니다.

            # 얼굴을 인식하여 리스트에 저장
            face_list = self.fd.detect_face(frame, 0)

            # 매치되는 얼굴이 있으면 리스트에 저장
            id_list = self.fm.match_face(face_list, './user/static/media/profile_pictures')

            # 타임스탬프에 찍기
            for id in id_list:
                save_attendance(id, self.camera_index)

            if self.camera_index == 1:
                cv2.imshow('출석관리 입구쪽', frame)
            else:
                cv2.imshow('출석관리 출구쪽', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

    def stop(self, **kwargs):
        self._stop_event.set()


# 서버 종료 시 카메라 작업 종료 처리
def stop_camera_task(sender, **kwargs):
    camera_task_stopped.send(sender=sender)


camera_task_stopped.connect(CameraBackgroundTask.stop)


def start(request):
    return redirect(home)


@csrf_exempt
def home(request):
    user = request.user
    userlist = UserList.objects.filter(student_id=user.id)

    start_time, end_time = get_class_time(userlist)

    in_time, out_time = get_inout_time(user)

    total, absent, early, late, out = get_class_days(user.id)

    return render(request, 'attendance/home.html', {'userlist': userlist,
                                                    'start_time': start_time, 'end_time': end_time,
                                                    'in_time': in_time, 'out_time': out_time,
                                                    'total': total, 'absent': absent, 'early': early,
                                                    'late': late, 'out': out})


@login_required
@csrf_exempt
def home_selected(request):
    data = json.loads(request.body)
    selected_date = data.get('selectedDate')
    selected_date = selected_date.split('T')[0]
    selected_log = Attendance.objects.filter(date=selected_date)
    user = request.user
    attendances = selected_log.filter(user_id=user.id)

    return render(request, 'attendance/table1.html', {'attendances': attendances})


def get_class_time(userlist):
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

    return start_time, end_time


def save_attendance(user_id, entering):
    userlist = UserList.objects.filter(student_id=user_id)
    start_time, end_time = get_class_time(userlist)

    is_entering = entering
    remark = attend_divide(user_id, is_entering, start_time, end_time)
    attendance = Attendance(is_entering=is_entering, remark=remark, user_id=user_id)
    try:
        prev_attendance = Attendance.objects.filter(Q(user_id=user_id) & Q(date=datetime.today().date())).latest('index')
        if prev_attendance.is_entering == entering:
            pass
        else:
            if prev_attendance.remark == '퇴실':
                pass
            elif datetime.now().time() > end_time:
                if prev_attendance.is_entering == 0:
                    prev_attendance.remark = '조퇴'
                    prev_attendance.save()
            else:
                attendance.save()
    except Attendance.DoesNotExist:
        if entering == 0:
            pass
        else:
            attendance.save()


def attend_divide(user_id, is_entering, start_time, end_time):
    attendance = Attendance.objects.filter(Q(user_id=user_id) & Q(date=datetime.today().date()))
    # When the user is entering the building
    if is_entering == 1:
        if not attendance:                                                  # if it is the first timestamp
            if datetime.now().time() <= start_time:                                   # if user arrived on time
                remark = '입실'
            else:                                                               # if user is late
                remark = '지각'
        else:                                                               # if it is not the first timestamp
            if attendance.latest('index').is_entering == False:
                comeback_time = attendance.filter(is_entering=0).latest('index').timestamp
                if datetime.now() - timedelta(hours=1) > datetime.combine(datetime.today().date(), comeback_time):
                    remark = '복귀'  # if user was outside for more than one hour
                    # 전 기록의 remark를 '외출'로 변경
                    attendance.filter(index=attendance.latest('index').index).update(remark='외출')
                else:  # if none of the those options
                    remark = ''
            else:
                remark = ''

    # When the user is exiting the building
    else:
        if datetime.now().time() >= end_time:
            remark = '퇴실'
        else:
            remark = ''
    return remark


def get_inout_time(user):
    user_attendances = Attendance.objects.filter(Q(user_id=user.id) & Q(date=datetime.today().date()))
    in_time_lis = user_attendances.filter(Q(remark='입실') | Q(remark='지각'))
    out_time_lis = user_attendances.filter(Q(remark='퇴실') | Q(remark='조퇴'))

    if in_time_lis:
        in_time = in_time_lis[0].timestamp
    else:
        in_time = ''

    if out_time_lis:
        out_time = out_time_lis[0].timestamp
    else:
        out_time = ''

    return in_time, out_time


def get_class_days(user_id):
    user_list = UserList.objects.filter(student_id=user_id)

    if not user_list:
        return 0, 0, 0, 0, 0

    attendance = Attendance.objects.filter(user_id=user_id).order_by('date')
    remove = Attendance.objects.filter(index=None)

    total_days = 0

    dates = [date for date, _ in groupby(attendance, key=lambda x: x.date)]
    for date in dates:
        filtered_attendance = attendance.filter(date=date)
        filtered_attendance.order_by('index')
        last_remark = filtered_attendance.order_by('index').last().remark
        if last_remark != '퇴실' and last_remark != '조퇴':
            remove = remove.union(filtered_attendance)
        else:
            total_days += 1
    attendance = attendance.exclude(index__in=remove.values('index'))

    early = attendance.filter(remark='조퇴').count()
    late = attendance.filter(remark='지각').count()
    out = attendance.filter(remark='외출').count()
    absent = total_class_days(user_list) - total_days
    total = total_days - early/3 - late/3 - out/3

    return round(total), absent, early, late, out


def total_class_days(userlist):
    class_id = userlist[0].class_id.id
    classtime = ClassTime.objects.filter(class_id_id=class_id).values()

    # 수업 없는 요일
    exclude_date = []
    count = -2 # because of 0: id, 1: class_id_id
    for key, value in classtime[0].items():
        if (value is None) & (key.endswith('_start')):
            exclude_date.append(math.floor(count / 2))
        count += 1

    start_date = userlist[0].class_id.start_date
    total = (datetime.today().date() - start_date).days

    total_days = 0
    for i in range(total):
        current_date = start_date + timedelta(days=i)
        if current_date.weekday() not in exclude_date:
            total_days += 1

    return total_days


def user_class(request):
    return render(request, 'user/class.html')
