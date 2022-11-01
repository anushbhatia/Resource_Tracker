from django.shortcuts import render, redirect
# Create your views here.
# def employee_list(request,template_name="employee_register\employee_list.html"): # Read
#   return render(request, template_name)
# def employee_form(request,template_name="employee_register\employee_form.html"): # Insert and update operations
#   return render(request, template_name)
# def employee_delete(request,template_name="employee_register\employee_form.html"): # Delete
#   return render(request, template_name)
from .models import Employee
# Create your views here.
def insert_emp(request,template_name="employee_register\employee_list.html"):  
  if request.method == "POST":       
    emp_code= request.POST['emp_code']       
    fullname = request.POST['fullname']       
    email = request.POST['email']       
    primary = request.POST['primary']       
    secondary= request.POST['secondary'] 
    location= request.POST['location']
    date=request.POST['date']
    remarks=request.POST['remarks']
    status=request.POST['status']
    designation=request.POST['designation']
    benchmng=request.POST['benchmng']  
    data = Employee(emp_code=emp_code, fullname=fullname, email=email, primary=primary, 
    secondary= secondary, location=location,date=date,remarks=remarks,status=status,designation=designation,
    benchmng=benchmng)        
    data.save()          
    return redirect('show/')    
  else:        
      return render(request, 'employee_register\index.html')
def show_emp(request):  
  employees = Employee.objects.all()    
  return render(request,'employee_register\show.html',{'employees':employees} )
def edit_emp(request):  
  return render(request, "employee_register\employee_list.html")
def remove_emp(request):
  return render(request, "employee_register\employee_list.html")



def demo_show(request):  
  return render(request, "employee_register\data-table.html")