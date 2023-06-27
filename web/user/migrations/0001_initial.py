# Generated by Django 4.2 on 2023-06-26 09:16

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, unique=True, verbose_name="이메일"),
                ),
                ("name", models.CharField(max_length=30, verbose_name="이름")),
                ("birthdate", models.DateField(verbose_name="생년월일")),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "남성"), ("W", "여성")],
                        max_length=10,
                        verbose_name="성별",
                    ),
                ),
                ("address", models.CharField(max_length=100, verbose_name="주소")),
                ("phone_number", models.CharField(max_length=20, verbose_name="전화번호")),
                (
                    "profile_picture",
                    models.ImageField(
                        upload_to="profile_pictures", verbose_name="프로필 사진"
                    ),
                ),
                ("is_staff", models.BooleanField(default=False, verbose_name="스태프 권한")),
                ("is_active", models.BooleanField(default=True, verbose_name="사용중")),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="가입일"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "swappable": "AUTH_USER_MODEL",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
