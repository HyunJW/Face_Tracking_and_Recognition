# Generated by Django 4.2 on 2023-06-27 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AcademyInfo",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100, verbose_name="학원명")),
                ("address", models.CharField(max_length=255, verbose_name="학원 주소")),
                ("tel", models.CharField(max_length=20, verbose_name="학원 연락처")),
            ],
            options={
                "db_table": "academy_info",
            },
        ),
        migrations.CreateModel(
            name="ClassInfo",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, verbose_name="과정명")),
                ("start_date", models.DateField(verbose_name="시작일")),
                (
                    "end_date",
                    models.DateField(blank=True, null=True, verbose_name="종료일"),
                ),
                (
                    "academy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="class_info",
                        to="attendance.academyinfo",
                    ),
                ),
            ],
            options={
                "db_table": "class_info",
            },
        ),
        migrations.CreateModel(
            name="ClassTime",
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
                (
                    "mon_start",
                    models.TimeField(blank=True, null=True, verbose_name="월요일 시작시간"),
                ),
                (
                    "mon_end",
                    models.TimeField(blank=True, null=True, verbose_name="월요일 종료시간"),
                ),
                (
                    "tue_start",
                    models.TimeField(blank=True, null=True, verbose_name="화요일 시작시간"),
                ),
                (
                    "tue_end",
                    models.TimeField(blank=True, null=True, verbose_name="화요일 종료시간"),
                ),
                (
                    "wed_start",
                    models.TimeField(blank=True, null=True, verbose_name="수월요일 시작시간"),
                ),
                (
                    "wed_end",
                    models.TimeField(blank=True, null=True, verbose_name="수월요일 종료시간"),
                ),
                (
                    "thu_start",
                    models.TimeField(blank=True, null=True, verbose_name="목요일 시작시간"),
                ),
                (
                    "thu_end",
                    models.TimeField(blank=True, null=True, verbose_name="목요일 종료시간"),
                ),
                (
                    "fri_start",
                    models.TimeField(blank=True, null=True, verbose_name="금월요일 시작시간"),
                ),
                (
                    "fri_end",
                    models.TimeField(blank=True, null=True, verbose_name="금요일 종료시간"),
                ),
                (
                    "sat_start",
                    models.TimeField(blank=True, null=True, verbose_name="토요일 시작시간"),
                ),
                (
                    "sat_end",
                    models.TimeField(blank=True, null=True, verbose_name="토요일 종료시간"),
                ),
                (
                    "sun_start",
                    models.TimeField(blank=True, null=True, verbose_name="일요일 시작시간"),
                ),
                (
                    "sun_end",
                    models.TimeField(blank=True, null=True, verbose_name="일요일 종료시간"),
                ),
                (
                    "class_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="time_table",
                        to="attendance.classinfo",
                    ),
                ),
            ],
            options={
                "db_table": "class_time",
            },
        ),
    ]