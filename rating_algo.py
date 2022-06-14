from quiz.models import *
from student.models import *


print(User)
def rating(username):
    #username=request.user.username
    userobj=User.objects.get(username=username)
    marks=Marks_Of_User.objects.filter(user=userobj)
    sum1=0
    weights={"PYTHON":10,"JAVA":10,"C++":10}
    for mark in marks:
        sum1+=mark.score*weights[mark.quiz.name]
    sum1//=3
    print(f"{username}:{sum1}")