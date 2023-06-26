from django.db import models
from user.models import User


class AttendanceDaily(models.Model):
    index = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_attendances')
    timestamp = models.DateTimeField()
    is_entering = models.BooleanField(default=False)
    remark = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'attendance_daily'


class AttendanceOverall(models.Model):
    overall_index = models.AutoField(primary_key=True)
    daily_index = models.IntegerField(unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='overall_attendances')
    timestamp = models.DateTimeField()
    is_entering = models.BooleanField(default=False)
    remark = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'attendance_overall'

