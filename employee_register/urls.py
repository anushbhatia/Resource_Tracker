from django.urls import path, include
from . import views

urlpatterns = [
   path('', views.home, name='home'), 
   path('insert/', views.insert_emp, name='insert-emp'), 
   path('show/', views.show_emp, name='show-emp'), 
   path('upload-csv/',views.profile_upload, name="profile_upload"),
   path('remove/', views.remove_emp, name='remove-emp'),
   path('editEmp/<emp_code>', views.edit_emp, name='edit-emp'),
   path('removeEmp/<emp_code>', views.remove_emp, name='remove-emp'),
   path('insertRequirement/',views.insert_requirement, name="insert_requirement"),
   path('showReq/', views.show_Req, name='show-Req'), 
]

