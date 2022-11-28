from django.shortcuts import render, redirect
from .models import Employee, Interviewer, Requirement
import csv, io
from django.contrib import messages
from django.core import serializers

# insert employee from form
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
    storage = messages.get_messages(request)
    storage.used = True
    return render(request, 'employee_register/profile_upload.html')

#Home page 
def home(request): 
  employees = Employee.objects.all()
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
def show_emp(request):  
  employees = Employee.objects.all()
  interviewers = serializers.serialize("json", Interviewer.objects.all())
  return render(request, "employee_register/showEmp.html",{'employees':employees,'interviewers':interviewers} )

#edit employee
def edit_emp(request,emp_code): 
  employee = Employee.objects.get(emp_code=emp_code)
  interviewers = Interviewer.objects.all()
  if request.method == 'POST':
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
    return redirect('/show')
  else:
    storage = messages.get_messages(request)
    storage.used = True
    return render(request,'employee_register/edit.html' ,{'employees':employee,'interviewers':interviewers})
  
#remove employee
def remove_emp(request,emp_code):
  employees = Employee.objects.get(emp_code=emp_code)
  employees.delete()
  messages.success(request, 'Profile deleted sucessfully.')
  return redirect('/show')
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
          'warningMsg': 'THIS IS NOT A CSV FILE',
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
    storage = messages.get_messages(request)
    storage.used = True
    return render(request, "employee_register/insertRequirement.html")
      
# show requirements
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