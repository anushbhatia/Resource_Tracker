# Generated by Django 4.1.2 on 2022-12-20 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_register', '0010_alter_employee_emptimestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='empTimeStamp',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
