from django.urls import path, include
from . import views

urlpatterns = [
   path('', views.home, name='home'), 
   path('insert/', views.insert_emp, name='insert-emp'), 
   path('show/', views.show_emp, name='show-emp'), 
   path('upload-csv/',views.profile_upload, name="profile_upload"),
   path('remove/', views.remove_emp, name='remove-emp'),
   path('login/', views.login_emp, name='login_emp'),
   path('edit/<emp_code>', views.edit_emp, name='edit-emp'),
   path('remove/<emp_code>', views.remove_emp, name='remove-emp')
]

