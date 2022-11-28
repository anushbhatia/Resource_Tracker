from django.urls import path, include
from . import views

urlpatterns = [
   #link of home page
   path('', views.home, name='home'),
   #links of employee
   path('insert/', views.insert_emp, name='insert-emp'), 
   path('upload-csv/',views.profile_upload, name="profile_upload"),
   path('show/', views.show_emp, name='show-emp'), 
   path('editEmp/<emp_code>', views.edit_emp, name='edit-emp'),
   path('removeEmp/<emp_code>', views.remove_emp, name='remove-emp'),
   #links of requirement
   path('insertRequirement/',views.insert_requirement, name="insert_requirement"),
   path('showReq/', views.show_Req, name='show-Req'), 
   path('editReq/<req_id>',views.edit_req,name='edit_req'),
   path('removeReq/<req_id>', views.remove_req, name='remove_req'),
]

