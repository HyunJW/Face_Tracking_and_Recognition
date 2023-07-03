from django.apps import AppConfig
import cv2
import threading


class AttendanceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "attendance"

    def ready(self):
        from attendance.views import CameraBackgroundTask
        from attendance.signals import camera_task_stopped

        # 서버 시작 시 카메라 작업 실행
        camera_task = CameraBackgroundTask()
        camera_task.start()

        # 서버 종료 시 카메라 작업 종료
        def stop_camera_task(sender, **kwargs):
            camera_task.stop()  # 작업을 종료하는 메서드 호출

        camera_task_stopped.connect(stop_camera_task)
