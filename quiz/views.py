from django.shortcuts import render, redirect
import sys
sys.path.append("..")
from .models import *
from student.models import StudentProfile
from django.http import JsonResponse,HttpResponse
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionForm
from django.forms import inlineformset_factory
from django.contrib import messages
from student.models import StudentProfile


def courses(request):
    return render(request,"courses.html")

def profile2(request):
    user = StudentProfile.objects.get(user= request.user)
    skills = user.get_skills()
    return render(request,"profile2.html",{'user':user,'skills':skills})


def index(request):
    quiz = Quiz.objects.all()
    user = request.user 
    marks = Marks_Of_User.objects.filter(user = user)
    para = {'quiz' : quiz,'marks': marks}
    return render(request, "index.html", para)

@login_required(login_url = '/login')
def quiz(request, myid):
    quiz = Quiz.objects.get(id=myid)
    return render(request, "quiz.html", {'quiz':quiz})


def quiz_data_view(request, myid):
    quiz = Quiz.objects.get(id=myid)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.content)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def save_quiz_view(request, myid):
    if is_ajax(request=request):
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(content=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(id=myid)

        score = 0
        marks = []
        correct_answer = None
        nqn=len(questions)
        for q in questions:
            a_selected = request.POST.get(q.content)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.content:
                        if a.correct:
                            score += 1
                            correct_answer = a.content
                    else:
                        if a.correct:
                            correct_answer = a.content

                marks.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                marks.append({str(q): 'not answered'})
        list_us = Marks_Of_User.objects.filter(quiz=quiz,user=user)
        score=(score/nqn)*100
        if(list_us):
            t = Marks_Of_User.objects.get(quiz=quiz,user=user)
            t.score = max(t.score,score)
            t.save()
        else:
            Marks_Of_User.objects.create(quiz=quiz, user=user, score=score)
        
        return JsonResponse({'passed': True, 'score': score, 'marks': marks})
    

# def Signup(request):
#     if request.user.is_authenticated:
#         return redirect('/')
#     if request.method=="POST":   
#         username = request.POST['username']
#         email = request.POST['email']
#         first_name=request.POST['first_name']
#         last_name=request.POST['last_name']
#         password = request.POST['password1']
#         confirm_password = request.POST['password2']
        
#         if password != confirm_password:
#             return redirect('/register')
        
#         user = User.objects.create_user(username, email, password)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()
#         return render(request, 'login.html')  
#     return render(request, "signup.html")

# def Login(request):
#     if request.user.is_authenticated:
#         return redirect('/')
#     if request.method=="POST":
#         username = request.POST['username']
#         password = request.POST['password']
        
#         user = authenticate(username=username, password=password)
        
#         if user is not None:
#             login(request, user)
#             return redirect("/")
#         else:
#             return render(request, "login.html") 
#     return render(request, "login.html")

# def Logout(request):
#     # logout(request)
#     return redirect('student:logout')


def add_quiz(request):
    if request.method=="POST":
        form = QuizForm(data=request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.save()
            obj = form.instance
            return render(request, "add_quiz.html", {'obj':obj})
    else:
        form=QuizForm()
    return render(request, "add_quiz.html", {'form':form})

def add_question(request):
    questions = Question.objects.all()
    questions = Question.objects.filter().order_by('-id')
    if request.method=="POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "add_question.html")
    else:
        form=QuestionForm()
    return render(request, "add_question.html", {'form':form, 'questions':questions})

def delete_question(request, myid):
    question = Question.objects.get(id=myid)
    if request.method == "POST":
        question.delete()
        return redirect('/quiz/add_question')
    return render(request, "delete_question.html", {'question':question})


def add_options(request, myid):
    question = Question.objects.get(id=myid)
    QuestionFormSet = inlineformset_factory(Question, Answer, fields=('content','correct', 'question'), extra=4)
    if request.method=="POST":
        formset = QuestionFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Your options are successfully saved !!')
            return render(request, "add_options.html")
    else:
        formset=QuestionFormSet(instance=question)
    return render(request, "add_options.html", {'formset':formset, 'question':question})

def results(request):
    marks = Marks_Of_User.objects.all()
    return render(request, "results.html", {'marks':marks})

def delete_result(request, myid):
    marks = Marks_Of_User.objects.get(id=myid)
    if request.method == "POST":
        marks.delete()
        return redirect('/quiz/results')
    return render(request, "delete_result.html", {'marks':marks})