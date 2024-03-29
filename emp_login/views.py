from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# login
def login_user(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      user = User.objects.get(username=username)
      last_login = user.last_login
      if last_login is not None:
        login(request, user)
        return redirect("../../")
      else:
        messages.success(request,'As a new user please set a new password.')
        return render(request, 'emp_login/passChange.html', {'username':username})
    else:
      messages.warning(request,"Invalid username or password. ")
      return redirect('../login/')
  else:
	  return render(request, 'emp_login/login.html')

# logout
@login_required(login_url="auth/login/")
def logout_user(request):
  logout(request)
  return redirect('../login/')

# password change for new user
def pass_change(request):
  if request.method == "POST":
    oldpass = request.POST['password1']
    newpass1 = request.POST['password2']
    newpass2 = request.POST['password3']
    username = request.POST['username']
    user = authenticate(username=username, password=oldpass)
    if user is not None:
      if newpass1 == newpass2:
        if newpass1 == oldpass:
          messages.warning(request,'Please do not use same password.')
          return redirect('../login/')
        else:
          login(request, user)
          u = User.objects.get(username=username)
          u.set_password(newpass1)
          u.save()
          logout(request)
          messages.success(request, "Password changed successfully. Please login again.")
          return redirect('../login/')
      else:
        messages.warning(request, 'Password not matching...')
        return redirect('../login/')
    else:
      messages.warning(request,"Old password incorrect. Please try again.")
      return redirect('../login/')
  else:
    return render(request, 'emp_login/passChange.html')


