from django.db import models
from user.models import User


class AttendanceDaily(models.Model):
    index = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_attendances')
    date = models.DateField('날짜', auto_now_add=True)
    timestamp = models.TimeField('시간', auto_now_add=True)
    is_entering = models.BooleanField('출입여부', default=False)
    remark = models.CharField('비고', max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'attendance_daily'


class AttendanceOverall(models.Model):
    overall_index = models.AutoField(primary_key=True)
    daily_index = models.IntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='overall_attendances')
    date = models.DateField('날짜')
    timestamp = models.TimeField('시간')
    is_entering = models.BooleanField('출입여부', default=False)
    remark = models.CharField('비고', max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'attendance_overall'


class AcademyInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('학원명', max_length=100)
    address = models.CharField('학원 주소', max_length=255)
    tel = models.CharField('학원 연락처', max_length=20)

    class Meta:
        db_table = "academy_info"


class ClassInfo(models.Model):
    id = models.AutoField(primary_key=True)
    academy = models.ForeignKey(AcademyInfo, on_delete=models.CASCADE, related_name='class_info')
    name = models.CharField('과정명', max_length=255)
    start_date = models.DateField('시작일')
    end_date = models.DateField('종료일', blank=True, null=True)

    class Meta:
        db_table = "class_info"


class ClassTime(models.Model):
    class_id = models.ForeignKey(ClassInfo, on_delete=models.CASCADE, related_name='time_table')
    mon_start = models.TimeField('월요일 시작시간', blank=True, null=True)
    mon_end = models.TimeField('월요일 종료시간', blank=True, null=True)
    tue_start = models.TimeField('화요일 시작시간', blank=True, null=True)
    tue_end = models.TimeField('화요일 종료시간', blank=True, null=True)
    wed_start = models.TimeField('수월요일 시작시간', blank=True, null=True)
    wed_end = models.TimeField('수월요일 종료시간', blank=True, null=True)
    thu_start = models.TimeField('목요일 시작시간', blank=True, null=True)
    thu_end = models.TimeField('목요일 종료시간', blank=True, null=True)
    fri_start = models.TimeField('금월요일 시작시간', blank=True, null=True)
    fri_end = models.TimeField('금요일 종료시간', blank=True, null=True)
    sat_start = models.TimeField('토요일 시작시간', blank=True, null=True)
    sat_end = models.TimeField('토요일 종료시간', blank=True, null=True)
    sun_start = models.TimeField('일요일 시작시간', blank=True, null=True)
    sun_end = models.TimeField('일요일 종료시간', blank=True, null=True)

    class Meta:
        db_table = "class_time"


class UserList(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_id")
    class_id = models.ForeignKey(ClassInfo, on_delete=models.CASCADE, related_name='class_taking')
    is_teacher = models.BooleanField(default=False)

    class Meta:
        db_table = "user_list"