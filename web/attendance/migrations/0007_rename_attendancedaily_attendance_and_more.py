# Generated by Django 4.2 on 2023-07-03 16:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("attendance", "0006_attendancedaily_date_attendanceoverall_date_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="AttendanceDaily",
            new_name="Attendance",
        ),
        migrations.AlterModelTable(
            name="attendance",
            table="attendance",
        ),
        migrations.DeleteModel(
            name="AttendanceOverall",
        ),
    ]
