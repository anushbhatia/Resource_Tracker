from django.urls import path, include
from . import views

urlpatterns = [
   path('', views.insert_emp, name='insert-emp'), 
   path('show/', views.show_emp, name='show-emp'), 
   path('edit/', views.edit_emp, name='edit-emp'), 
   path('upload-csv/',views.profile_upload, name="profile_upload"),
   path('remove/', views.remove_emp, name='remove-emp'),

   path('demo_show/', views.demo_show, name='show-emp'),
]

