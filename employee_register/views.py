from django.shortcuts import render
# Create your views here.
def employee_list(request,template_name="employee_register\employee_list.html"): # Read
  return render(request, template_name)
def employee_form(request,template_name="employee_register\employee_form.html"): # Insert and update operations
  return render(request, template_name)
def employee_delete(request,template_name="employee_register\employee_form.html"): # Delete
  return render(request, template_name)