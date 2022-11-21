from django.db import models
from datetime import date
# Create your models here.
class Interviewer(models.Model):
    name=models.CharField(max_length=100)
    skill=models.CharField(max_length=100)
    count=models.CharField(max_length=100,default=0)

class Employee(models.Model):
    emp_code = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    primary=models.CharField(max_length=100)
    secondary=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    designation=models.CharField(max_length=100)
    benchmng=models.CharField(max_length=100)
    remarks=models.CharField(max_length=200)
    status=models.CharField(max_length=100,default='NA')
    panel=models.CharField(max_length=100,default='NA')
    date=models.DateField(default=date.today)
class Meta:        
    db_table="Employee"

# Forward ForeignKey relationship
#Employee.objects.select_related('status').all()
 
# Reverse ForeignKey relationship
#EmpStatus.objects.prefetch_related('Employee').all()
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
