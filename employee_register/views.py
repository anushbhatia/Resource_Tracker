from django.shortcuts import render, redirect
from .models import Employee
from .models import EmpStatus
import csv, io
from django.contrib import messages

# insert view page for form
def insert_emp(request,template_name="employee_register\employee_list.html"):  
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
      #remarks=request.POST['remarks']
      #status=request.POST['status']
      designation=request.POST['designation']
      benchmng=request.POST['benchmng']  
      data = Employee(emp_code=emp_code, fullname=fullname, email=email, primary=primary, 
      secondary= secondary, location=location,status_id=1, designation=designation,
      benchmng=benchmng)        
      data.save()          
      return redirect('../upload-csv/')
    else:
      
      return render(request, 'employee_register\profile_upload.html')
  else:        
      return render(request, 'employee_register\profile_upload.html')

#Home page view
def home(request): 
  employees = Employee.objects.all()
  profileCount = 0
  for employee in employees:
    profileCount = profileCount+1
  
  return render(request, "employee_register\home.html",{'profileCount':profileCount})

#show page view
def show_emp(request):  
  employees = Employee.objects.all()
  return render(request, "employee_register\data-table.html",{'employees':employees} )

#edit page view
def edit_emp(request):  
  return render(request, "employee_register\employee_list.html")
  
#remove page view
def remove_emp(request):
  return render(request, "employee_register\employee_list.html")


# insert page view for csv upload
# one parameter named request
def profile_upload(request):
      template = "employee_register\profile_upload.html"
      data = Employee.objects.all()
      # prompt is a context variable that can have different values depending on their context
      prompt = {
          'order': 'Order of the CSV should be name, email, address, phone, profile',
          'profiles': data    
                }
      # GET request returns the value of the data with the specified key.
      if request.method == "GET":
          return render(request, template, prompt)
      csv_file = request.FILES['file']
      # let's check if it is a csv file
      if not csv_file.name.endswith('.csv'):
          messages.error(request, 'THIS IS NOT A CSV FILE')
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
        date= column[6],
        remarks=column[7],
        status=column[8],
        designation=column[9],
        benchmng=column[10] 
        )
      context = {}
      return render(request, template, context)

#Login page view
def login_emp(request):
   return render(request, "employee_register\login.html")
      


  
