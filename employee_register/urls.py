from django.urls import path, include
from . import views
app_name = 'employee_register'
urlpatterns = [
   #link of home page
   path('', views.home, name='home'),
   #link of add user page
   path('viewUser/',views.view_user, name="view_user"),
   path('register/',views.register_user, name="register_user"),
   path('removeUser/<int:user_id>',views.remove_user,name='remove_user'),
   path('editUser/<int:user_id>',views.edit_user,name='edit_user'),
   #link of my profile
   path('profile/',views.show_profile,name="show_profile"),
   path('passChange/',views.pass_change,name="pass_change"),
   path('editProfile/',views.edit_profile,name='edit_profile'),
   #links of employee
   path('insert/', views.insert_emp, name='insert_emp'), 
   path('upload-csv/',views.profile_upload, name="profile_upload"),
   path('show/', views.show_emp, name='show-emp'), 
   path('editEmp/<emp_code>', views.edit_emp, name='edit_emp'),
   path('editEmpInt/<emp_code>', views.edit_emp_int, name='edit-emp-int'),
   path('removeEmp/<emp_code>', views.remove_emp, name='remove_emp'),
   #links of requirement
   path('insertRequirement/',views.insert_requirement, name="insert_requirement"),
   path('showReq/', views.show_Req, name='show_Req'), 
   path('editReq/<req_id>',views.edit_req,name='edit_req'),
   path('removeReq/<req_id>',views.remove_req, name='remove_req'),
]

