import time
from django.shortcuts import render, redirect
from datetime import datetime as dtime
from .models import Employee, Interviewer, Requirement
import csv, io
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required,permission_required
from django.core import serializers
from django.core.mail import send_mail
import json
from datetime import datetime

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

# Insert employee from form
@login_required(login_url="auth/login/")
@permission_required('employee_register.add_employee', raise_exception=True)
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
      empCVPath=request.POST['empCVPath']
      data = Employee(emp_code=emp_code, empFullname=empFullname, empEmail=empEmail, empPrimary=empPrimary, 
      empSecondary= empSecondary, empLocation=empLocation, empDesignation=empDesignation,
      empBenchmng=empBenchmng,CVPath=empCVPath)        
      data.save()          
      messages.success(request, 'Profile added sucessfully. ')
      return redirect('../upload-csv/')
    else:
      messages.warning(request, 'Employee with same Id already exist. ')
      return redirect('../upload-csv/')
  else:   
    return render(request, 'employee_register/profile_upload.html')

# Home page 
@login_required(login_url="auth/login/")
def home(request): 
  employees = Employee.objects.all()
  profileCount = 0 
  deployedCount = 0
  progessCount = 0
  rejectCount = 0

  selected_primary_tech_dict =    {}
  in_progress_primary_tech_dict = {}
  rejected_primary_tech_dict =    {}
  monthly_selected_dict = {'Jan':0,'Feb':0,'Mar':0,'Apr':0,'May':0,'June':0,'Jul':0,'Aug':0,'Sep':0,'Oct':0,'Nov':0,'Dec':0}
  monthly_in_progress_dict = {'Jan':0,'Feb':0,'Mar':0,'Apr':0,'May':0,'June':0,'Jul':0,'Aug':0,'Sep':0,'Oct':0,'Nov':0,'Dec':0}
  monthly_rejected_dict = {'Jan':0,'Feb':0,'Mar':0,'Apr':0,'May':0,'June':0,'Jul':0,'Aug':0,'Sep':0,'Oct':0,'Nov':0,'Dec':0}
  months = ['Jan','Feb','Mar','Apr','May','June','Aug','Sep','Oct','Nov','Dec']

  all_tech = []


  for employee in employees:
    profileCount = profileCount+1
    if(employee.empStatus=='Client Select'):
      deployedCount=deployedCount+1
      if (employee.empTimeStamp is not None):
        month = employee.empTimeStamp.month
        month = months[month-1]
        monthly_selected_dict[month] = monthly_selected_dict[month] + 1
      else:
        pass
        
      
    elif(employee.empStatus=='NA' or employee.empStatus=='L1 Assigned' or employee.empStatus=='L1 Select'):
      progessCount=progessCount+1
      if (employee.empTimeStamp is not None):
        month = employee.empTimeStamp.month
        month = months[month-1]
        monthly_in_progress_dict[month] = monthly_in_progress_dict[month]+1
      else:
        month = employee.empDate.month
        month = months[month-1]
        monthly_in_progress_dict[month] = monthly_in_progress_dict[month]+1

    elif(employee.empStatus=='L1 Reject' or employee.empStatus=='Client Reject' or employee.empStatus=='Others'):
      rejectCount=rejectCount+1
      if (employee.empTimeStamp is not None):
        month = employee.empTimeStamp.month
        month = months[month-1]
        monthly_rejected_dict[month] = monthly_rejected_dict[month] + 1
      else:
        pass
    
    if(employee.empPrimary in in_progress_primary_tech_dict.keys() and (employee.empStatus=='NA' or employee.empStatus=='L1 Assigned' or employee.empStatus=='L1 Select')):
      in_progress_primary_tech_dict[employee.empPrimary] = in_progress_primary_tech_dict[employee.empPrimary] + 1
    elif(employee.empPrimary not in in_progress_primary_tech_dict.keys() and (employee.empStatus=='NA' or employee.empStatus=='L1 Assigned' or employee.empStatus=='L1 Select')):
      in_progress_primary_tech_dict[employee.empPrimary] = 1


    if(employee.empPrimary in selected_primary_tech_dict.keys() and employee.empStatus=='Client Select'):
      selected_primary_tech_dict[employee.empPrimary] = selected_primary_tech_dict[employee.empPrimary] + 1
    elif(employee.empPrimary not in selected_primary_tech_dict.keys() and employee.empStatus=='Client Select'):
      selected_primary_tech_dict[employee.empPrimary] = 1


    if(employee.empPrimary in rejected_primary_tech_dict.keys() and (employee.empStatus=='L1 Reject' or employee.empStatus=='Client Reject' or employee.empStatus=='Others')):
      rejected_primary_tech_dict[employee.empPrimary] = rejected_primary_tech_dict[employee.empPrimary] + 1
    elif(employee.empPrimary not in rejected_primary_tech_dict.keys() and (employee.empStatus=='L1 Reject' or employee.empStatus=='Client Reject' or employee.empStatus=='Others')):
      rejected_primary_tech_dict[employee.empPrimary] = 1

  for keys in in_progress_primary_tech_dict.keys():
    all_tech.append(keys)
  
  for keys in selected_primary_tech_dict.keys():
    all_tech.append(keys)
    
  for keys in rejected_primary_tech_dict.keys():
    all_tech.append(keys)
  
  
  all_tech = set(all_tech)
  all_tech = sorted(all_tech)

  selected_tech_dict_json = json.dumps(selected_primary_tech_dict)
  in_progress_tech_dict_json = json.dumps(in_progress_primary_tech_dict)
  rejected_tech_dict_json = json.dumps(rejected_primary_tech_dict)

  return render(request, "employee_register/home.html",{'profileCount':profileCount,'deployedCount':deployedCount,'progessCount':progessCount,'rejectCount':rejectCount,'selected_primary_tech_dict':selected_primary_tech_dict,'in_progress_primary_tech_dict':in_progress_primary_tech_dict,'rejected_primary_tech_dict':rejected_primary_tech_dict,'all_tech':all_tech,'selected_tech_dict_json':selected_tech_dict_json,'in_progress_tech_dict_json':in_progress_tech_dict_json,'rejected_tech_dict_json':rejected_tech_dict_json,'monthly_in_progress_dict':monthly_in_progress_dict,'monthly_rejected_dict':monthly_rejected_dict,'monthly_selected_dict':monthly_selected_dict})

class Interviewerc(object):
        def __init__(self, interviewer_id, name):
            self.interviewer_id = interviewer_id
            self.name = name

# Show employee 
@login_required(login_url="auth/login/")
@permission_required('employee_register.view_employee', raise_exception=True)
def show_emp(request): 
  employees = Employee.objects.all()
  interviewers = serializers.serialize("json", Interviewer.objects.all())
  return render(request, "employee_register/showEmp.html",{'employees':employees,'interviewers':interviewers} )

# Edit employee
@login_required(login_url="auth/login/")
@permission_required('employee_register.change_employee', raise_exception=True)
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
    #temppanel=employee.empPanel
    #employee.empPanel=request.POST['empPanel']
    employee.CVPath=request.POST['empCVPath']
    #print(employee.empPanel)
    employee.empDesignation=request.POST['empDesignation']
    employee.empBenchmng=request.POST['empBenchmng']
    temppanel=employee.interviewer
    newpanel=request.POST['empPanel']
    if(temppanel!=newpanel):
      for i in interviewers:
        if(i.name==newpanel and employee.empStatus=='NA' and i.name!='NA'):
          employee.interviewer=i
          employee.empStatus='L1 Assigned'
          
        elif(i.name==newpanel and employee.empStatus!='NA' and i.name=='NA'):
          employee.interviewer=i
          employee.empStatus='NA' 
        elif(i.name==newpanel):
          employee.interviewer=i
    # for i in interviewers:
    #   print(temppanel,employee.empPanel,i.name,employee.empPanel,employee.empStatus)
    #   if(temppanel!=employee.empPanel and i.name==employee.empPanel and employee.empStatus=='NA' and i.name!='NA'):
    #     employee.interviewer=i
    #     employee.empStatus='L1 Assigned'
        
    #   elif(temppanel!=employee.empPanel and i.name==employee.empPanel and employee.empStatus!='NA' and i.name=='NA'):
    #     employee.interviewer=i
    #     employee.empStatus='NA' 
    #   elif(temppanel!=employee.empPanel and i.name==employee.empPanel):
    #     employee.interviewer=i
    employee.empTimeStamp=datetime.now()
    employee.save() 
    messages.success(request, 'Profile updated sucessfully. ')
    count_interview()
    return redirect('../show')
  else:
    
    return redirect('../show')
  
# Edit employee by interviewer
@login_required(login_url="auth/login/")
@permission_required('employee_register.change_employee', raise_exception=True)
def edit_emp_int(request,emp_code): 
  interviewers = Interviewer.objects.all()
  if request.method == 'POST':
    employee = Employee.objects.get(emp_code=emp_code)
    #employee.emp_code= request.POST['emp_code'] 
    employee.empRemarks=request.POST['empRemarks']
    employee.empStatus=request.POST['empStatus']
    temppanel=employee.interviewer
    newpanel=request.POST['empPanel']
    if(temppanel!=newpanel):
      for i in interviewers:
        if(i.name==newpanel and employee.empStatus=='NA' and i.name!='NA'):
          employee.interviewer=i
          employee.empStatus='L1 Assigned'
          
        elif(i.name==newpanel and employee.empStatus!='NA' and i.name=='NA'):
          employee.interviewer=i
          employee.empStatus='NA' 
        elif(i.name==newpanel):
          employee.interviewer=i
    employee.empTimeStamp=datetime.now()
    employee.save() 
    messages.success(request, 'Profile updated sucessfully. ')
    count_interview()
    
    return redirect('../show')
  else:
    return redirect('../show')
 
# Remove employee
@login_required(login_url="auth/login/")
@permission_required('employee_register.delete_employee', raise_exception=True)
def remove_emp(request,emp_code):
  employees = Employee.objects.get(emp_code=emp_code)
  employees.delete()
  messages.success(request, 'Profile deleted sucessfully. ')
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
@permission_required('employee_register.add_employee', raise_exception=True)
def profile_upload(request):
      template = "employee_register/profile_upload.html"
      countadd=0
      countskip=0
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
          messages.warning(request, 'This is NOT a CSV file ')
          prompt = {
          'profiles': data 
                }
          return redirect('../upload-csv/')
      data_set = csv_file.read().decode('UTF-8')
      # setup a stream which is when we loop through each line we are able to handle a data in a stream
      io_string = io.StringIO(data_set)
      next(io_string)
      for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        empId =None
        try:
          empId = Employee.objects.get(emp_code=column[0])
        except:
          pass
        if(empId==None):
          countadd=countadd+1
          _, created = Employee.objects.update_or_create(
          emp_code= column[0],      
          empFullname = column[1],      
          empEmail = column[2],    
          empPrimary = column[3],       
          empSecondary= column[4],
          empLocation= column[5],
          empDesignation=column[6],
          empBenchmng=column[7],
          CVPath=column[8]
        )
        else:
          countskip=countskip+1

      context = {}
      a='Profiles from csv added sucessfully.Profiles Added: '+str(countadd) +" Profiles Skipped: " +str(countskip)
      messages.success(request, a)
      return render(request, template, context)

# Insert requirements
@login_required(login_url="auth/login/")
@permission_required('employee_register.add_requirement', raise_exception=True)
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
      messages.success(request, 'requirement added sucessfully. ')
      return redirect('../insertRequirement/')
  else:   
    return render(request, "employee_register/insertRequirement.html")
      
# Show requirements
@login_required(login_url="auth/login/")
@permission_required('employee_register.view_requirement', raise_exception=True)
def show_Req(request):
  requirements = Requirement.objects.all()
  return render(request, "employee_register/showReq.html", {'requirements':requirements})

def count_interview():
  interviewers = Interviewer.objects.all()
  employees = Employee.objects.all()
  for interviewer in interviewers:
    count=0
    for employee in employees:
      if(interviewer.interviewer_id==employee.interviewer_id and employee.empStatus=='L1 Assigned' and interviewer.interviewer_id!=0 ):
        count=count+1
      elif(interviewer.interviewer_id==employee.interviewer_id and employee.interviewer_id==0):
        count=count+1
    interviewer.count=count
    interviewer.save()

# Edit requirement
@login_required(login_url="auth/login/")
@permission_required('employee_register.change_requirement', raise_exception=True)
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
    messages.success(request, 'Requirement updated sucessfully. ')
    return redirect('/showReq')
  else:
    return redirect('/showReq')

# Remove requirement
@login_required(login_url="auth/login/")
@permission_required('employee_register.delete_requirement', raise_exception=True)
def remove_req(request,req_id):
  requirement = Requirement.objects.get(id=req_id)
  requirement.delete()
  messages.success(request, 'Requirement deleted sucessfully. ')
  return redirect('/showReq')

# Add new(register) user  
@login_required(login_url="auth/login/")
@permission_required('auth.add_user', raise_exception=True)
@permission_required('employee_register.add_interviewer', raise_exception=True)
def register_user(request):
  if request.method == 'POST':
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    userType = request.POST['userType']
    if password1 == password2:
      if User.objects.filter(username=username).exists():
        messages.warning(request, 'Username already taken. ')
        return redirect('../viewUser/')
      elif User.objects.filter(email=email).exists():
        messages.warning(request, 'Email already exists. ')
        return redirect('../viewUser/')
      elif User.objects.filter(first_name=first_name, last_name=last_name).exists():
        messages.warning(request, 'User with same name already exists. ')
        return redirect('../viewUser/')
      else:
        user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        user.save()
        my_group = Group.objects.get(name=userType) 
        my_group.user_set.add(user)
        print(userType)
        if userType == "Interviewer":
          name= first_name +' '+ last_name     
          skill = request.POST['skill'] 
          userId=User.objects.get(username=username)
          data = Interviewer(name=name,skill=skill,user_id=userId.id)
          data.save()
        messages.success(request, 'User added successfully. ')
        return redirect('../viewUser/')
    else:
      messages.warning(request, 'Password not matching... ')
      return redirect('../viewUser/')
  else:
    return redirect('../viewUser/')

# View Users
@login_required(login_url="auth/login/")
@permission_required('auth.view_user', raise_exception=True)
@permission_required('employee_register.view_interviewer', raise_exception=True)
def view_user(request):
  users = User.objects.all()
  groups = Group.objects.all()
  editGroup = serializers.serialize("json", Group.objects.all())
  interviwer = serializers.serialize("json", Interviewer.objects.all())
  return render(request, "employee_register/users.html", {'userList':users,'grouplist':groups,'editGroupList':editGroup,'interviwer':interviwer})

# Edit user  
@login_required(login_url="auth/login/")
@permission_required('auth.change_user', raise_exception=True)
@permission_required('employee_register.change_interviewer', raise_exception=True)
def edit_user(request,user_id):
  if request.method == 'POST':
    user = User.objects.get(id=user_id)
    oldFirstName = user.first_name
    oldLastName = user.last_name
    oldUsername = user.username
    oldEmail = user.email
    oldUserType = user.groups.all()[0].name
    newFirstName = request.POST['userFirstName']
    newLastName = request.POST['userLastName']
    newUsername = request.POST['userUsername']
    newEmail = request.POST['userEmail']
    newUserType = request.POST['userUserType']
    if(oldFirstName!=newFirstName or oldLastName!=newLastName):
      if User.objects.filter(first_name=newFirstName, last_name=newLastName).exists():
        messages.warning(request, 'User with same name already exists. ')
        return redirect('../register')
      else:
        user.first_name = newFirstName
        user.last_name = newLastName
    if(oldUsername!=newUsername):
      if User.objects.filter(username=newUsername).exists():
        messages.warning(request, 'Username already taken. ')
        return redirect('../register')
      else:
        user.username = newUsername
    if(oldEmail!=newEmail):
      if User.objects.filter(email=newEmail).exists():
        messages.warning(request, 'Email already exists. ')
        return redirect('../register')
      else:
        user.email = newEmail
    if(oldUserType!=newUserType):
      group1 = Group.objects.get(name=oldUserType)
      user.groups.remove(group1)
      group2 = Group.objects.get(name=newUserType)
      user.groups.add(group2)
      if oldUserType == "Interviewer":
        data = Interviewer.objects.get(user_id=user_id)
        data.delete()
      if newUserType == "Interviewer":
        name= user.first_name +' '+ user.last_name    
        skill = request.POST['userSkill'] 
        data = Interviewer(name=name,skill=skill,user_id=user_id)
        data.save()
    user.save()
    messages.success(request, 'User updated successfully. ')
    return redirect('../viewUser')
  else:
    return redirect('../viewUser')

# Remove user
@login_required(login_url="auth/login/")
@permission_required('auth.delete_user', raise_exception=True)
@permission_required('employee_register.delete_interviewer', raise_exception=True)
def remove_user(request,user_id):
  user = User.objects.get(id=user_id)
  user.delete()
  messages.success(request, 'User deleted sucessfully. ')
  return redirect('../viewUser')

# Show my profile
@login_required(login_url="auth/login/")
def show_profile(request):
  permissionList=[]
  try: #Added for the superuser
    grpName=request.user.groups.all()[0]
  except:
    grpName=Group.objects.all()[2]
  allPerm = grpName.permissions.all()
  for perm in allPerm:
    p=str(perm).split('|')
    permissionList.append(p[2])
  return render(request,'employee_register/profile.html',{'permList':permissionList})

# My password change
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
          messages.warning(request,'Please do not use same password. ')
          return redirect('../profile/')
        else:
          u = User.objects.get(username=username)
          u.set_password(newpass1)
          u.save()
          messages.success(request, "Password changed successfully. Please login again. ")
          return redirect('../auth/login/')
      else:
        messages.warning(request, 'Password not matching... ')
        return redirect('../profile/')
    else:
      messages.warning(request,"Old password is incorrect. ")
      return redirect('../profile/')
  else:
    return redirect('../profile/')

# Edit my profile
@login_required(login_url="auth/login/")
def edit_profile(request):
  if request.method == 'POST':
    userId = request.user.id
    myProfile = User.objects.get(id=userId)
    tempFirstName = myProfile.first_name
    tempLastName = myProfile.last_name
    tempEmail = myProfile.email
    newFirstName = request.POST['userFirstName']
    newLastName = request.POST['userLastName']
    newEmail = request.POST['userEmail']
    if tempFirstName != newFirstName or tempLastName != newLastName:
      if User.objects.filter(first_name=newFirstName, last_name=newLastName).exists():
        messages.warning(request, 'User with same name already exists. ')
        return redirect('../profile/')
      else:
        myProfile.first_name = newFirstName
        myProfile.last_name = newLastName
    if tempEmail!=newEmail:
      if User.objects.filter(email=newEmail).exists():
        messages.warning(request, 'Email already exists. ')
        return redirect('../profile/')
      else:
        myProfile.email = newEmail
    myProfile.save()
    messages.success(request, 'Profile updated sucessfully. ')
    return redirect('../profile/')
  else:
   
    return redirect('../profile/')
 
# send_mail(subject = 'Test Mail',message = 'Kindly Ignore',from_email = 'anushbhatia1234@gmail.com',recipient_list = ['anushbhatia1234@gmail.com'],fail_silently = False);
# while True:
#     now = dtime.now()
#   # If the time now is 15:15 run the rest.
#     if now.hour == 10 and now.minute == 30:
#         interviewers = Interviewer.objects.all()
#         users=User.objects.all()
#         for interviewer in interviewers:
#           for user in users:
#             if user.id==interviewer.user_id:
#                 print(user.email)
#                 htmlmessage=f'''Hi {user.first_name} 👋, <br>
#                 <p>You have been assigned {interviewer.count} profiles for the review.Please Evaluate the profiles as earliest as possible.<br>
#                 <a href="http://abhatia1.pythonanywhere.com/" target="_blank">View Profiles</a></button><br></p>
#                 Thanks and Regards,<br>
#                 Profile Team 🤖'''
#                 send_mail(subject = 'New Profiles For Review',
#                 message='You have been assigned profiles for the review.',
#                 html_message= htmlmessage
#                 ,from_email = 'anushbhatia1234@gmail.com',recipient_list = [user.email],fail_silently = False)
#                 time.sleep(3600)
#     if now.hour == 17 and now.minute == 00:
#         interviewers = Interviewer.objects.all()
#         users=User.objects.all()
#         for interviewer in interviewers:
#           for user in users:
#             if user.id==interviewer.user_id:
#                 print(user.email)
#                 htmlmessage=f'''Hi {user.first_name} 👋, <br>
#                 <p>You have been assigned {interviewer.count} profiles for the review.Please Evaluate the profiles as earliest as possible.<br>
#                 <a href="http://abhatia1.pythonanywhere.com/" target="_blank">View Profiles</a></button><br></p>
#                 Thanks and Regards,<br>
#                 Profile Team 🤖'''
#                 send_mail(subject = 'New Profiles For Review',
#                 message='You have been assigned profiles for the review.',
#                 html_message= htmlmessage
#                 ,from_email = 'anushbhatia1234@gmail.com',recipient_list = [user.email],fail_silently = False)
#                 time.sleep(3600)

        