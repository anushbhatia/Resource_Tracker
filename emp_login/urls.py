from django.urls import path, include
from . import views

urlpatterns = [
    #link of login page
   path('login/', views.login_user, name='login_user'),
#    path('register/',views.register, name="register"),
   path('logout/',views.logout_user, name="logout_user"),
   path('passChange/',views.pass_change,name="pass_change"),
]