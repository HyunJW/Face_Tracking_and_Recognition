# Generated by Django 4.2 on 2023-06-28 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_alter_user_is_staff"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(
                upload_to="profile_pictures/", verbose_name="프로필 사진"
            ),
        ),
    ]
