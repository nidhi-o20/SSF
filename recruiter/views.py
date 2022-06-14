from django.db import models
from django.shortcuts import render,redirect
from .models import RecruiterProfile
from student.models import StudentProfile, Skills
from quiz.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.

def signin(request):
    # if request.user.is_authenticated:
    #     return redirect("/recruiter")
    if request.method == 'POST':
        username = request.POST['username'].upper()
        password = request.POST['password']
       # user = User.objects.filter(username=username).first()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            ruser = RecruiterProfile.objects.get(user=request.user)
            priority1 = ruser.priority1
            priority2 = ruser.priority2
            priority3 = ruser.priority3
            weights = {priority1:3, priority2: 2, priority3: 1}
            rankings = getAllRatings(weights)
            return render(request, 'rank.html', {'priority1': priority1, 'priority2': priority2, 'priority3': priority3,"students":rankings})
        else:
            return HttpResponse('no such user exists')

    else:
        return render(request, 'rlogin.html')



def home(request):
    return render(request, 'home.html', {})


def getAllRatings(weights):
    stdobjs=StudentProfile.objects.all()
    # weights={"PYTHON":10,"JAVA":10,"C++":10}
    ranking={}
    for obj in stdobjs:
        ranking[obj.username]=rating(obj.username,weights)
    temp=[(v,k) for k,v in ranking.items()]
    temp.sort(reverse=True)
    temp=[{'name':v,"val":k}for (k,v) in temp]
    print(temp)
    return temp


def rating(username,weights):
    #username=request.user.username
    userobj=User.objects.get(username=username)
    marks=Marks_Of_User.objects.filter(user=userobj)
    sum1=0
    for mark in marks:
        sum1+=mark.score*weights[(mark.quiz.name).upper()]
    sum1//=3
    return sum1



def dashboard(request):
    return render(request, 'dashboard.html')


def RecruiterSignup(request):
    skills = Skills.objects.all()
    if request.method == 'POST':
        company = request.POST['company']
        bio = request.POST['bio']
        location = request.POST['location']
        priority1 = request.POST['priority1']
        priority2 = request.POST['priority2']
        priority3 = request.POST['priority3']
        password = request.POST['password']

        user_profile = RecruiterProfile.objects.filter(username=company)
        if user_profile.exists():
            return HttpResponse('error')
        else:
            user = User.objects.create(
                username=company.upper(), password=password)
            user.save()
            user_object = User.objects.get(
                username=company.upper(), password=password)
            user_object.set_password(password)
            user_object.save()
            user_profile = RecruiterProfile.objects.create(user=user_object, username=company.upper(
            ), bio=bio, location=location, priority1=priority1, priority2=priority2, priority3=priority3)

            user_profile.save()
            # rankings=getAllRatings()
            return redirect('rlogin')
            # return render(request, 'rank.html', {'priority1': priority1, 'priority2': priority2, 'priority3': priority3,"students":rankings})
    else:
        context = {'skills': skills}
        return render(request, 'profile.html', context)


def mail(request):
    send_mail(
        'Testing..',
        'Message.',
        '2019nidhi.thakkar@ves.ac.in',
        ['nthakkar2010@gmail.com'],
    )
    return render(request, 'mail.html')



def signout(request):
    logout(request)
    return redirect('/')