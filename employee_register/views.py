from django.shortcuts import render, redirect
from .models import Employee, Interviewer, Requirement
import csv, io
from django.contrib import messages

# insert view page for form
def insert_emp(request,template_name="employee_register/employee_list.html"):  
  if request.method == "POST":  
    empId = None
    try:
      empId = Employee.objects.get(emp_code=request.POST['emp_code'])
    except:
      pass
    if(empId==None):
      emp_code= request.POST['emp_code']       
      fullname = request.POST['fullname']       
      email = request.POST['email']       
      primary = request.POST['primary']       
      secondary= request.POST['secondary'] 
      location= request.POST['location']
      designation=request.POST['designation']
      benchmng=request.POST['benchmng']  
      data = Employee(emp_code=emp_code, fullname=fullname, email=email, primary=primary, 
      secondary= secondary, location=location, designation=designation,
      benchmng=benchmng)        
      data.save()          
      messages.success(request, 'Profile added sucessfully.')
      return redirect('../upload-csv/')
    else:
      empId= request.POST['emp_code']
      employee = Employee.objects.get(emp_code=empId)

      employee.fullname = request.POST['fullname']       
      employee.email = request.POST['email']       
      employee.primary = request.POST['primary']       
      employee.secondary= request.POST['secondary'] 
      employee.location= request.POST['location']
      employee.designation=request.POST['designation']
      employee.benchmng=request.POST['benchmng']
      employee.save() 
      messages.success(request, 'Profile updated sucessfully.')
      return render(request, 'employee_register/profile_upload.html')
  else:   
    storage = messages.get_messages(request)
    for _ in storage: 
        pass
    return render(request, 'employee_register/profile_upload.html')

#Home page view
def home(request): 
  employees = Employee.objects.all()
  profileCount = 0
  deployedCount = 0
  progessCount = 0
  rejectCount = 0
  for employee in employees:
    profileCount = profileCount+1
    if(employee.status=='Client Select'):
      deployedCount=deployedCount+1
    elif(employee.status=='NA' or employee.status=='L1 Assigned' or employee.status=='L1 Select'):
      progessCount=progessCount+1
    elif(employee.status=='L1 Reject' or employee.status=='Client Reject' or employee.status=='Others'):
      rejectCount=rejectCount+1

  return render(request, "employee_register/home.html",{'profileCount':profileCount,'deployedCount':deployedCount,'progessCount':progessCount,'rejectCount':rejectCount})

#show page view
def show_emp(request):  
  employees = Employee.objects.all()
  interviewers = Interviewer.objects.values('name')
  return render(request, "employee_register/showEmp.html",{'employees':employees,'interveiwers':interviewers} )

#edit page view
def edit_emp(request,emp_code): 
  print('hi') 
  employee = Employee.objects.get(emp_code=emp_code)
  interviewers = Interviewer.objects.values('name')
  if request.method == 'POST':
    #employee.emp_code= request.POST['emp_code']       
    employee.fullname = request.POST['fullname']       
    employee.email = request.POST['email']       
    employee.primary = request.POST['primary']       
    employee.secondary= request.POST['secondary'] 
    employee.location= request.POST['location']
    employee.remarks=request.POST['remarks']
    employee.status=request.POST['status']
    employee.panel=request.POST['panel']
    employee.designation=request.POST['designation']
    employee.benchmng=request.POST['benchmng']
    employee.save() 
    messages.success(request, 'Profile updated sucessfully.')
    return redirect('/show')
  else:
    storage = messages.get_messages(request)
    for _ in storage: 
        pass
    return render(request,'employee_register/edit.html' ''',{'employees':employee,'interviewers':interviewers}''')
  
#remove page view
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


# insert page view for csv upload
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
        fullname = column[1],      
        email = column[2],    
        primary = column[3],       
        secondary= column[4],
        location= column[5],
        designation=column[6],
        benchmng=column[7],
        )
      context = {}
      messages.success(request, 'Profiles from csv added sucessfully.')
      return render(request, template, context)

def insert_requirement(request):
  if request.method == "POST":  
      requestor= request.POST['requestor']       
      primary = request.POST['primary']       
      secondary = request.POST['secondary']       
      location = request.POST['location']       
      grade= request.POST['grade'] 
      reqCount= request.POST['reqCount'] 
      reqData = Requirement(requestor=requestor,primary=primary,secondary=secondary,location=location,grade=grade,reqCount=reqCount)      
      reqData.save()          
      messages.success(request, 'requirement added sucessfully.')
      return redirect('../insertRequirement/')
  else:   
    storage = messages.get_messages(request)
    for _ in storage: 
        pass
    return render(request, "employee_register/insertRequirement.html")
      


  
