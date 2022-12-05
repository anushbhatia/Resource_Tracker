from django.shortcuts import render, redirect
from .models import Employee, Interviewer, Requirement
import csv, io
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core import serializers
'''
LOCATION: 30
GRADE:30
IF PRIMARY: 30 THEN SECONDARY: 10
'''
def profile_percentange():
  percent=0
  employees = Employee.objects.all()
  requirements=Requirement.objects.all()
  for employee in employees:
    for requirement in requirements:
      if(employee.empDesignation==requirement.reqGrade and employee.empPrimary.lower()==requirement.reqPrimary.lower()):
        percent=50
  return percent

# insert employee from form
@login_required(login_url="auth/login/")
def insert_emp(request,template_name="employee_register/employee_list.html"):  
  if request.method == "POST":  
    empId = None
    try:
      empId = Employee.objects.get(emp_code=request.POST['emp_code'])
    except:
      pass
    if(empId==None):
      emp_code= request.POST['emp_code']       
      empFullname = request.POST['empFullname']       
      empEmail = request.POST['empEmail']       
      empPrimary = request.POST['empPrimary']       
      empSecondary= request.POST['empSecondary'] 
      empLocation= request.POST['empLocation']
      empDesignation=request.POST['empDesignation']
      empBenchmng=request.POST['empBenchmng']  
      data = Employee(emp_code=emp_code, empFullname=empFullname, empEmail=empEmail, empPrimary=empPrimary, 
      empSecondary= empSecondary, empLocation=empLocation, empDesignation=empDesignation,
      empBenchmng=empBenchmng)        
      data.save()          
      messages.success(request, 'Profile added sucessfully.')
      return redirect('../upload-csv/')
    else:
      empId= request.POST['emp_code']
      employee = Employee.objects.get(emp_code=empId)

      employee.empFullname = request.POST['empFullname']       
      employee.empEmail = request.POST['empEmail']       
      employee.empPrimary = request.POST['empPrimary']       
      employee.empSecondary= request.POST['empSecondary'] 
      employee.empLocation= request.POST['empLocation']
      employee.empDesignation=request.POST['empDesignation']
      employee.empBenchmng=request.POST['empBenchmng']
      employee.save() 
      messages.success(request, 'Profile updated sucessfully.')
      return render(request, 'employee_register/profile_upload.html')
  else:   
    return render(request, 'employee_register/profile_upload.html')

#Home page 
@login_required(login_url="auth/login/")
def home(request): 
  employees = Employee.objects.all()
  # userName = request.user.get_full_name()
  profileCount = 0 
  deployedCount = 0
  progessCount = 0
  rejectCount = 0
  for employee in employees:
    profileCount = profileCount+1
    if(employee.empStatus=='Client Select'):
      deployedCount=deployedCount+1
    elif(employee.empStatus=='NA' or employee.empStatus=='L1 Assigned' or employee.empStatus=='L1 Select'):
      progessCount=progessCount+1
    elif(employee.empStatus=='L1 Reject' or employee.empStatus=='Client Reject' or employee.empStatus=='Others'):
      rejectCount=rejectCount+1

  return render(request, "employee_register/home.html",{'profileCount':profileCount,'deployedCount':deployedCount,'progessCount':progessCount,'rejectCount':rejectCount})

class Interviewerc(object):
        def __init__(self, interviewer_id, name):
            self.interviewer_id = interviewer_id
            self.name = name

#show employee 
@login_required(login_url="auth/login/")
def show_emp(request): 
  employees = Employee.objects.all()
  interviewers = serializers.serialize("json", Interviewer.objects.all())
  return render(request, "employee_register/showEmp.html",{'employees':employees,'interviewers':interviewers} )

#edit employee
@login_required(login_url="auth/login/")
def edit_emp(request,emp_code): 
  interviewers = Interviewer.objects.all()
  if request.method == 'POST':
    employee = Employee.objects.get(emp_code=emp_code)
    #employee.emp_code= request.POST['emp_code']       
    employee.empFullname = request.POST['empFullname']       
    employee.empEmail = request.POST['empEmail']       
    employee.empPrimary = request.POST['empPrimary']       
    employee.empSecondary= request.POST['empSecondary'] 
    employee.empLocation= request.POST['empLocation']
    employee.empRemarks=request.POST['empRemarks']
    employee.empStatus=request.POST['empStatus']
    temppanel=employee.empPanel
    employee.empPanel=request.POST['empPanel']
    employee.empDesignation=request.POST['empDesignation']
    employee.empBenchmng=request.POST['empBenchmng']
    for i in interviewers:
      print(temppanel,employee.empPanel,i.name,employee.empPanel,employee.empStatus)
      if(temppanel!=employee.empPanel and i.name==employee.empPanel and employee.empStatus=='NA' and i.name!='NA'):
        employee.interviewer=i
        employee.empStatus='L1 Assigned'
      elif(temppanel!=employee.empPanel and i.name==employee.empPanel and employee.empStatus!='NA' and i.name=='NA'):
        employee.interviewer=i
        employee.empStatus='NA' 
      elif(temppanel!=employee.empPanel and i.name==employee.empPanel):
        employee.interviewer=i
    employee.save() 
    messages.success(request, 'Profile updated sucessfully.')
    count_interview()
    return redirect('../show')
  else:
    employees = Employee.objects.all()
    interviewers = Interviewer.objects.values('name')
    return render(request,'employee_register/showEmp.html' ,{'employees':employees,'interviewers':interviewers})
  
#remove employee
@login_required(login_url="auth/login/")
def remove_emp(request,emp_code):
  employees = Employee.objects.get(emp_code=emp_code)
  employees.delete()
  messages.success(request, 'Profile deleted sucessfully.')
  return redirect('../show')
  '''#if we use post contidition using form popup
  if request.method == 'POST':
      employees.delete()
      return redirect('/show')

  context = {
        'employees': employees,
        'interviewers':interviewers
  }
  
  return render(request, 'employee_register/delete.html', context)
  '''

# insert employee from csv upload
# one parameter named request
@login_required(login_url="auth/login/")
def profile_upload(request):
      template = "employee_register/profile_upload.html"
      data = Employee.objects.all()
      # prompt is a context variable that can have different values depending on their context
      prompt = {
          'order': 'Order of the CSV should be:- Id, Name, Email, Primary skill, Secondary skill, Location, Designation, Bench manager',
          'profiles': data   
                }
      # GET request returns the value of the data with the specified key.
      if request.method == "GET":
          return render(request, template, prompt)
      csv_file = request.FILES['file']
      # let's check if it is a csv file
      if not csv_file.name.endswith('.csv'):
          messages.error(request, 'THIS IS NOT A CSV FILE')
          prompt = {
          'profiles': data 
                }
          return redirect('../upload-csv/')
      data_set = csv_file.read().decode('UTF-8')
      # setup a stream which is when we loop through each line we are able to handle a data in a stream
      io_string = io.StringIO(data_set)
      next(io_string)
      for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Employee.objects.update_or_create(
        emp_code= column[0],      
        empFullname = column[1],      
        empEmail = column[2],    
        empPrimary = column[3],       
        empSecondary= column[4],
        empLocation= column[5],
        empDesignation=column[6],
        empBenchmng=column[7],
        )
      context = {}
      messages.success(request, 'Profiles from csv added sucessfully.')
      return render(request, template, context)

# insert requirements
@login_required(login_url="auth/login/")
def insert_requirement(request):
  if request.method == "POST":  
      requestor= request.POST['requestor']       
      reqPrimary = request.POST['reqPrimary']       
      reqSecondary = request.POST['reqSecondary']       
      reqLocation = request.POST['reqLocation']       
      reqGrade= request.POST['reqGrade'] 
      reqCount= request.POST['reqCount'] 
      reqData = Requirement(requestor=requestor,reqPrimary=reqPrimary,reqSecondary=reqSecondary,reqLocation=reqLocation,reqGrade=reqGrade,reqCount=reqCount)      
      reqData.save()          
      messages.success(request, 'requirement added sucessfully.')
      return redirect('../insertRequirement/')
  else:   
    return render(request, "employee_register/insertRequirement.html")
      
# show requirements
@login_required(login_url="auth/login/")
def show_Req(request):
  requirements = Requirement.objects.all()
  return render(request, "employee_register/showReq.html", {'requirements':requirements})

def count_interview():
  interviewers = Interviewer.objects.all()
  employees = Employee.objects.all()
  for interviewer in interviewers:
    count=0
    for employee in employees:
      if(interviewer.interviewer_id==employee.interviewer):
        count=count+1
    interviewer.count=count
    interviewer.save()

# Edit requirement
@login_required(login_url="auth/login/")
def edit_req(request,req_id): 
  if request.method == 'POST':
    requirement = Requirement.objects.get(id=req_id)
    requirement.requestor = request.POST['requestor']       
    requirement.reqPrimary = request.POST['reqPrimary']       
    requirement.reqSecondary = request.POST['reqSecondary']       
    requirement.reqLocation= request.POST['reqLocation'] 
    requirement.reqGrade= request.POST['reqGrade']
    requirement.reqCount=request.POST['reqCount']
    requirement.save() 
    messages.success(request, 'Requirement updated sucessfully.')
    return redirect('/showReq')
  else:
    requirements = Requirement.objects.all()
    return render(request,'employee_register/showReq.html' ,{'requirements':requirements})

# remove requirement
@login_required(login_url="auth/login/")
def remove_req(request,req_id):
  requirement = Requirement.objects.get(id=req_id)
  requirement.delete()
  messages.success(request, 'Requirement deleted sucessfully.')
  return redirect('/showReq')

# register  
@login_required(login_url="login/")
def register(request):
  if request.method == 'POST':
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    if password1 == password2:
      if User.objects.filter(username=username).exists():
        messages.warning(request, 'Username already taken.')
        return redirect('../register/')
      elif User.objects.filter(email=email).exists():
        messages.warning(request, 'Email already exists.')
        return redirect('../register/')
      elif User.objects.filter(first_name=first_name, last_name=last_name).exists():
        messages.warning(request, 'User with same name already exists')
        return redirect('../register/')
      else:
        user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        user.save()
        userType = request.POST['userType']
        if userType == "interviewer":
          name= first_name +' '+ last_name     
          skill = request.POST['skill'] 
          data = Interviewer(name=name,skill=skill)
          data.save()
        messages.success(request, 'User added successfully.')
        return redirect('../register/')
    else:
      messages.warning(request, 'Password not matching...')
      return redirect('../register/')
  else:
    return render(request, "employee_register/register.html")

# password change
@login_required(login_url="auth/login/")
def pass_change(request):
  if request.method == "POST":
    username = request.user.get_username()
    oldpass = request.POST['password1']
    newpass1 = request.POST['password2']
    newpass2 = request.POST['password3']
    userAuth = authenticate(username=username, password=oldpass)
    if userAuth is not None:
      if newpass1 == newpass2:
        if newpass1 == oldpass:
          messages.warning(request,'Please do not use same password.')
          return redirect('../passChange/')
        else:
          u = User.objects.get(username=username)
          u.set_password(newpass1)
          u.save()
          messages.success(request, "Password changed successfully. Please login again.")
          return redirect('../login/')
      else:
        messages.warning(request, 'Password not matching...')
        return redirect('../passChange/')
    else:
      messages.error(request,"Old password is incorrect")
      return redirect('../passChange/')
  else:
    return render(request, 'employee_register/passChange.html')
