from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    profile_picture = profile_picture = models.ImageField()
    groups = models.ManyToManyField(Group, related_name='user_attendance', blank=True, db_table='user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_attendance', blank=True,
                                              db_table='user_user_permissions')

    class Meta:
        db_table = 'attendance_user'


class AttendanceDaily(models.Model):
    index = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_attendances')
    timestamp = models.DateTimeField()
    is_entering = models.BooleanField(default=False)
    remark = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'attendance_daily'


class AttendanceOverall(models.Model):
    overall_index = models.AutoField(primary_key=True)
    daily_index = models.IntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='overall_attendances')
    timestamp = models.DateTimeField()
    is_entering = models.BooleanField(default=False)
    remark = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'attendance_overall'

