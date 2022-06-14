from django.urls import path
from . import views
app_name = 'quiz'
urlpatterns = [
    path("", views.index, name="index"),
    

    path("<int:myid>/", views.quiz, name="quiz"), 
    path('<int:myid>/data/', views.quiz_data_view, name='quiz-data'),
    path('<int:myid>/save/', views.save_quiz_view, name='quiz-save'),
    
    # path("signup", views.Signup, name="signup"),
    # path("login", views.Login, name="login"),
    # path("logout", views.Logout, name="logout"),
    path('courses/',views.courses,name="courses"),
    path('profile2/',views.profile2,name="profile2"),
    path('/quiz/add_quiz/', views.add_quiz, name='add_quiz'),    
    path('/quiz/add_question/', views.add_question, name='add_question'),  
    path('/quiz/add_options/<int:myid>/', views.add_options, name='add_options'), 
    path('/quiz/results/', views.results, name='results'),
    path('/quiz/delete_question/<int:myid>/', views.delete_question, name='delete_question'),  
    path('/quiz/delete_result/<int:myid>/', views.delete_result, name='delete_result'),
]