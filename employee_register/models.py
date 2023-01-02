from django.db import models
from datetime import date
# Create your models here.
class Interviewer(models.Model):
    interviewer_id=models.AutoField(primary_key=True)
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
    interviewer=models.ForeignKey(Interviewer,on_delete=models.PROTECT,default=1)
class Meta:        
    db_table="Employee"

class Requirement(models.Model):
    requestor=models.CharField(max_length=100)
    reqPrimary=models.CharField(max_length=100)
    reqSecondary=models.CharField(max_length=100)
    reqEmail=models.CharField(max_length=100)
    reqLocation=models.CharField(max_length=100)
    reqGrade=models.CharField(max_length=10)
    reqCount=models.SmallIntegerField()