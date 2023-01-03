# Generated by Django 4.1.2 on 2022-12-19 07:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee_register', '0007_alter_employee_emptimestamp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interviewer',
            name='user_id',
        ),
        migrations.AddField(
            model_name='interviewer',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='employee',
            name='empTimeStamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 19, 13, 9, 21, 508960)),
        ),
    ]
