# Generated by Django 4.1.2 on 2022-11-23 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_register', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestor', models.CharField(max_length=100)),
                ('primary', models.CharField(max_length=100)),
                ('secondary', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('grade', models.CharField(max_length=10)),
                ('reqCount', models.SmallIntegerField()),
            ],
        ),
    ]