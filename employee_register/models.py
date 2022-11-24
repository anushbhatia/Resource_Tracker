from django.db import models
from datetime import date
# Create your models here.
class Interviewer(models.Model):
    name=models.CharField(max_length=100)
    skill=models.CharField(max_length=100)
    count=models.CharField(max_length=100,default=0)

class Employee(models.Model):
    emp_code=models.CharField(max_length=100)
    empFullname=models.CharField(max_length=100)
    empEmail=models.CharField(max_length=100)
    empPrimary=models.CharField(max_length=100)
    empSecondary=models.CharField(max_length=100)
    empLocation=models.CharField(max_length=100)
    empDesignation=models.CharField(max_length=100)
    empBenchmng=models.CharField(max_length=100)
    empRemarks=models.CharField(max_length=200)
    empStatus=models.CharField(max_length=100,default='NA')
    empPanel=models.CharField(max_length=100,default='NA')
    empDate=models.DateField(default=date.today)
class Meta:        
    db_table="Employee"

class Requirement(models.Model):
    requestor=models.CharField(max_length=100)
    reqPrimary=models.CharField(max_length=100)
    reqSecondary=models.CharField(max_length=100)
    reqLocation=models.CharField(max_length=100)
    reqGrade=models.CharField(max_length=10)
    reqCount=models.SmallIntegerField()
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
