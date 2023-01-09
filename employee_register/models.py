from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
# Interviewer Model
class Interviewer(models.Model):
    interviewer_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    skill=models.CharField(max_length=100)
    count=models.CharField(max_length=100,default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None,null=True)
    def __str__(self):
        return self.name
    @classmethod
    def get_default_pk(cls):
        interviewer, created = cls.objects.get_or_create(
            name='NA', 
            skill='NA',
            count=0,
        )
        return interviewer.pk
class Meta:        
    db_table="Interviewer"
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
    empPanel=models.CharField(max_length=100,default='NA') # need to remove
    empDate=models.DateField(default=date.today)  # date on which record added
    interviewer=models.ForeignKey(Interviewer,on_delete=models.SET_DEFAULT,default=Interviewer.get_default_pk)
    empTimeStamp = models.DateTimeField(default=None,null=True)  #date on which L1 assigned 
class Meta:        
    db_table="Employee"
# Requirement Model
class Requirement(models.Model):
    requestor=models.CharField(max_length=100)
    reqPrimary=models.CharField(max_length=100)
    reqSecondary=models.CharField(max_length=100)
    reqEmail=models.CharField(max_length=100)
    reqLocation=models.CharField(max_length=100)
    reqGrade=models.CharField(max_length=10)
    reqCount=models.SmallIntegerField()
class Meta:        
    db_table="Requirement"




