# Generated by Django 4.1.2 on 2023-01-17 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_register', '0002_employee_cvpath_alter_employee_interviewer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='CVPath',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
