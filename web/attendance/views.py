from datetime import datetime
from django.shortcuts import render, redirect
from attendance.models import Attendance, UserList, ClassTime
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
        # cap = cv2.VideoCapture('d:/video/enter.mp4') # 동영상 사용

        while not self._stop_event.is_set():
            ret, frame = cap.read()  # 영상 프레임을 읽어옵니다.

            # 얼굴을 인식하여 리스트에 저장
            face_lis = self.fd.detect_face(frame, 0)

            # 매치되는 얼굴이 있으면 리스트에 저장
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


def save_attendance(user_id):
    userlist = UserList.objects.filter(student_id=user_id)
    start_time, end_time = get_class_time(userlist)

    is_entering = 1
    remark = attend_divide(user_id, is_entering, start_time, end_time)
    attendance = Attendance(is_entering=is_entering, remark=remark, user_id=user)
    prev_attendance = Attendance.objects.filter(Q(user_id=user_id) & Q(date=datetime.today().date()))[-1]
    if prev_attendance.remark == '퇴실':
        pass
    elif datetime.time() > end_time:
        if prev_attendance.is_entering == 0:
            prev_attendance.remark = '조퇴'
            prev_attendance.save()
    else:
        attendance.save()


def attend_divide(user_id, is_entering, start_time, end_time):
    attendance = Attendance.objects.filter(Q(user_id=user_id) & Q(date=datetime.today().date()))
    # When the user is entering the building
    if is_entering == 1:
        if not attendance:                                                  # if it is the first timestamp
            if datetime.time() <= start_time:                                   # if user arrived on time
                remark = '입실'
            else:                                                               # if user is late
                remark = '지각'
        else:                                                               # if it is not the first timestamp
            if datetime.now() - timedelta(hours=1) > attendance.filter(is_entering=0)[-1].timestamp:
                remark = '복귀'                                                  # if user was outside for more than one hour
                # 전 기록의 remark를 '외출'로 변경
                attendance[-1].remark = '외출'
                attendance[-1].save()
            else:                                                               # if none of the those options
                remark = ''

    # When the user is exiting the building
    else:
        if datetime.time() >= end_time:
            remark = '퇴실'
        else:
            remark = ''
    return remark


def get_inout_time(user):
    user_attendances = Attendance.objects.filter(Q(user_id=user.id) & Q(date=datetime.today().date()))
    if user_attendances:
        try:
            in_attend = user_attendances.filter(is_entering=1)
            in_time = in_attend[0].timestamp
            current_in_time = in_attend.latest('timestamp').timestamp
        except:
            in_time = '조회할 수 없습니다.'
        try:
            out_attend = user_attendances.filter(is_entering=0)
            out_time = out_attend.latest('timestamp').timestamp
            if in_time != '조회할 수 없습니다.':
                if current_in_time > out_time:
                    out_time = ''
        except:
            out_time = ''

    else:
        in_time = ''
        out_time = ''
    return in_time, out_time


def user_class(request):
    return render(request, 'user/class.html')
