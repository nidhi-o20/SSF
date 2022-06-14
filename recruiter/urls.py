from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('signup', views.RecruiterSignup, name='recruiter-signup'),
    path("ratings", views.getAllRatings, name="rating"),
    path('', views.home, name='recruiter-home'),
    path('dashboard/', views.dashboard, name='recruiter-dashboard'),
    path('mail', views.mail, name='mail'),
    path('login/',views.signin,name='rlogin'),
    path('logout/',views.signout,name='rlogout')

]
