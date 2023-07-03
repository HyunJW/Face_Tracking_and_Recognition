from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import AttendanceDaily, UserList, ClassTime
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

User = get_user_model()


class CameraBackgroundTask(threading.Thread):
    def __init__(self):
        super(CameraBackgroundTask, self).__init__()
        self._stop_event = threading.Event()
        self.fd = FaceDetect()
        self.fm = FaceMatch()

    def run(self):
        cap = cv2.VideoCapture(0)  # 웹캠에 접근하기 위해 0을 사용합니다.

        while not self._stop_event.is_set():
            ret, frame = cap.read()  # 영상 프레임을 읽어옵니다.

            # 얼굴을 인식하여 리스트에 저장
            face_lis = self.fd.detect_face(frame, 1)
            id_list = self.fm.match_face(face_lis, './user/static/media/profile_pictures')
            # 타임스탬프에 찍기
            for id in id_list:
                save_attendance(id)

            cv2.imshow('Camera', frame)

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

    return render(request, 'attendance/home.html', {'userlist': userlist,
                                                    'start_time': start_time, 'end_time': end_time,
                                                    'in_time': in_time, 'out_time': out_time})


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


def save_attendance(user_id):
    user = User.objects.get(id=user_id)
    userlist = UserList.objects.filter(student_id=user_id)
    start_time, end_time = get_class_time(userlist)

    is_entering = 1
    remark = attend_divide(is_entering, start_time, end_time)
    attendance = AttendanceDaily(is_entering=is_entering,
                                 remark=remark,
                                 user_id=user)
    attendance.save()


def attend_divide(is_entering, start_time, end_time):
    if is_entering == 1:
        if datetime.time() <= start_time:
            remark = '입실'  # User is entering
        else:
            remark = '지각'  # User is late (or returning)
    elif is_entering == 0:
        if datetime.time() >= end_time:
            remark = '퇴실'
        else:
            remark = '조퇴'
    return remark


def get_inout_time(user):
    user_attendances = AttendanceDaily.objects.filter(Q(user_id=user.id) & Q(date=datetime.today().date()))

    if user_attendances:
        # in_time = user_attendances.filter(remark='입실')[0].timestamp
        # out_time = user_attendances.filter(remark='퇴실')[0].timestamp
        in_time = ''
        out_time = ''
    else:
        in_time = ''
        out_time = ''
    return in_time, out_time


def user_class(request):
    return render(request, 'user/class.html')



