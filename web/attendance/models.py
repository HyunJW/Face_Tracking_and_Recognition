from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class AttendanceUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일을 입력하세요')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pictures')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['age', 'gender', 'address', 'phone_number', 'profile_picture']

    objects = AttendanceUserManager()


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

