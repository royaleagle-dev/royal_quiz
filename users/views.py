from django.shortcuts import render, redirect
#from users.forms import SignupForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login
from users.models import Profile, PendingQuestion
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail
from quiz.models import Question, Category, Subject
import datetime


# Create your views here.

def approve(request, pk):
    pQuestion = PendingQuestion.objects.get(pk = pk)
    category = Category.objects.get(title = pQuestion.category)
    subject = Subject.objects.get(title = pQuestion.subject)
    q = Question (title = pQuestion.question, pub_date = datetime.datetime.now().date(), category = category, subject = subject )
    q.save()
    pQuestion.delete()
    return redirect('users:dashboard', username = request.user.username)
    
def decline(request, pk):
    pQuestion = PendingQuestion.objects.get(pk=pk)
    pQuestion.delete()
    messages.success (request, 'Question successfully deleted from database.')
    return redirect('users:dashboard', username = request.user.username)

@login_required
def pendingQuestion(request, username):
    user = request.user
    if user.profile.status == 'au':
        question = PendingQuestion.objects.filter(is_approved__exact = False).order_by('-id')
        question_count = PendingQuestion.objects.filter(is_approved__exact = False).count()
        ctx = {
            'question':question,
            'question_count':question_count
        }
        return render(request, 'users/pendingQuestions.html', ctx)
    else:
        messages.error (request, 'sorry you do not have the permission to view this page')
        return redirect ('users:dashboard')


@login_required
def addQuestion(request, username):
    category = Category.objects.all()
    subject = Subject.objects.all()
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        subject = request.POST.get('subject')
        category = request.POST.get('category')
        answer = request.POST.get('answer')
        
        question = PendingQuestion(question = question, option1 = option1, option2 = option2, option3 = option3, option4 = option4, sender = request.user.username, is_approved = False, category = category, subject = subject, answer = answer )
        question.save()
        messages.success (request, 'Question successfully submitted, and is under processing. The question will be added to the database after processing is complete')
        return redirect('users:dashboard', username = request.user.username)
    else:
        ctx = {
        'category':category,
        'subject':subject,
        }
        return render(request, 'users/addQuestion.html', ctx)

def profileUpdate(request, username):
    user = User.objects.get(username = username)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        
        user.username = username
        user.password = password
        user.email = email
        user.save()
        
        user.profile.firstname = firstname
        user.profile.lastname = lastname
        user.save()
        return redirect('users:profile', username = username)
        

def profile(request, username):
    user = User.objects.get(username = username)
    ctx = {
        'user':user
    }
    return render(request, 'users/profile.html', ctx)

'''def profileMini(request, username):
    user = User.objects.get(username = username)
    ctx = {
        'user':user
    }
    return render(request, 'users/profileMini.html', ctx)
    '''

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get ('email')

        try:
            user = User.objects.create_user(username = username, password = password, email = email)
            user.save()
            user.profile.firstname = request.POST.get('firstname')
            user.profile.lastname = request.POST.get('lastname')
            user.status = 'bu'
            user.save()
            messages.success(request, 'Account successfully created')
            return redirect ('users:coreLogin')

        except IntegrityError:
            messages.warning(request, 'Please choose another username, the username already exists')
            return redirect('users:signup')
    else:
        return render(request, 'registration/signup.html')

def coreLogin(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            profile = Profile.objects.get_or_create(user = user)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('users:dashboard', username = username)
                else:
                    messages.warning(request, 'your account has been disabled temporarily, pls contact the admin')
            else:
                messages.warning(request, 'your account is not found in the pls re-register')
                return redirect('users:coreLogin')
        
        except IntegrityError:
            messages.error(request, 'pls fill in the correct credentials')
            return redirect('users:coreLogin')
    else:
        return render(request, 'registration/login.html')
            
@login_required
def dashboard(request, username):
    user = User.objects.get(username = username)
    question_count = Question.objects.all().count()
    category_count = Category.objects.all().count()
    subject_count = Subject.objects.all().count()
    user_count = User.objects.all().count()
    #total quiz done by a user
    total_quiz_count = user.profile.total_quiz_count
    today = datetime.datetime.now()
    today_date = (int(today.year), int(today.month), int(today.day))
    new_question_count = Question.objects.filter(pub_date__date = datetime.date(today_date[0], today_date[1], today_date[2])).count()
    new_user_count = User.objects.filter(date_joined__date = datetime.date(today_date[0], today_date[1], today_date[2])).count()

    ctx = {
    'question_count':question_count,
    'category_count':category_count,
    'subject_count':subject_count,
    'user_count': user_count,
    'total_quiz_count': total_quiz_count,
    'user': user,
    'new_question_count':new_question_count,
    'new_user_count': new_user_count,
    }
    return render(request, 'users/dashboard.html', ctx)

class dashboardUsers(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/dashboardUsers.html'
    queryset = User.objects.all().order_by('-profile__RP')
    paginate_by = 12

class scoreBoard(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/scoreBoard.html'
    queryset = User.objects.all().order_by('-profile__RP')[:5]

@login_required
def dashboardQuiz(request):
    user = request.user
    ctx = {
        'user':user,
    }
    return render(request, 'users/dboard_base.html', ctx)