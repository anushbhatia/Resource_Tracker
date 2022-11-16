from django.db import models
# Create your models here.
class Position(models.Model):
   title = models.CharField(max_length=50)
   
class Employee(models.Model):
    emp_code = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    primary=models.CharField(max_length=100)
    secondary=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    remarks=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    designation=models.CharField(max_length=100)
    benchmng=models.CharField(max_length=100)
class Meta:        
    db_table="Employee"
'''
KID/User ID
Name
Email
Primary Skill
Secondary Skill
Location
Date
Remarks
Approve Reject (Status)
Designation
Add by (bench manager name.
    emp_code = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    primary=models.CharField(max_length=100)
    seondary=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    date=models.DateField()
    remarks=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    designation=models.CharField(max_length=100)
    benchmng=models.CharField(max_length=100)
'''
