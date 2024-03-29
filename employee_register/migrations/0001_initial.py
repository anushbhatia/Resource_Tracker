# Generated by Django 4.1.2 on 2023-01-29 07:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import employee_register.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestor', models.CharField(max_length=100)),
                ('reqPrimary', models.CharField(max_length=100)),
                ('reqSecondary', models.CharField(max_length=100)),
                ('reqEmail', models.CharField(max_length=100)),
                ('reqLocation', models.CharField(max_length=100)),
                ('reqGrade', models.CharField(max_length=10)),
                ('reqCount', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Interviewer',
            fields=[
                ('interviewer_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('skill', models.CharField(max_length=100)),
                ('count', models.CharField(default=0, max_length=100)),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_code', models.CharField(max_length=100)),
                ('empFullname', models.CharField(max_length=100)),
                ('empEmail', models.CharField(max_length=100)),
                ('empPrimary', models.CharField(max_length=100)),
                ('empSecondary', models.CharField(max_length=100)),
                ('empLocation', models.CharField(max_length=100)),
                ('empDesignation', models.CharField(max_length=100)),
                ('empBenchmng', models.CharField(max_length=100)),
                ('empRemarks', models.CharField(max_length=200)),
                ('empStatus', models.CharField(default='NA', max_length=100)),
                ('empDate', models.DateField(default=datetime.date.today)),
                ('empTimeStamp', models.DateTimeField(default=None, null=True)),
                ('CVPath', models.CharField(max_length=200)),
                ('interviewer', models.ForeignKey(default=employee_register.models.Interviewer.get_default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='employee_register.interviewer')),
            ],
        ),
    ]
