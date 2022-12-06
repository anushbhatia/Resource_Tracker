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
        login(request, user)
        logout(request)
        messages.warning(request,'As a new user please set a new password.')
        return render(request, 'emp_login/passChange.html', {'username':username})
    else:
      messages.error(request,"Invalid username or password.")
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
    username = request.user.get_username()
    oldpass = request.POST['password1']
    newpass1 = request.POST['password2']
    newpass2 = request.POST['password3']
    username = request.POST['username']
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
    return render(request, 'emp_login/passChange.html')


