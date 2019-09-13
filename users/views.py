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


# Create your views here.
@login_required
def approveQuestion(request):
    user = request.user
    if user.profile.status == 'au':
        question = PendingQuestion.objects.filter(is_approved__exact = False)
        question_count = PendingQuestion.objects.filter(is_approved__exact = False).count()
        ctx = {
            'question':question,
            'question_count':question_count
        }
        return render(request, 'users/approveQuestion.html', ctx)
    else:
        messages.error (request, 'sorry you do not have the permission to view this page')
        return redirect ('index')


@login_required
def addQuestion(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        
        question = PendingQuestion(question = question, option1 = option1, option2 = option2, option3 = option3, option4 = option4, sender = request.user.username, is_approved = False )
        
        question.save()
        
        messages.success (request, 'Question successfully submitted, and is under processing. The question will be added to the database after processing is complete')
        
        return redirect('users:profile', username = request.user.username)
    else:
        messages.error (reqeust, "you are not permitted be view this page")
        return redirect ('index')

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

def profileMini(request, username):
    user = User.objects.get(username = username)
    ctx = {
        'user':user
    }
    return render(request, 'users/profileMini.html', ctx)

def signup(request):
    return render(request, 'registration/signup.html')

def signup_processor(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    
    if len(email) == 0:
        messages.warning(request, 'pls input a valid email')
        return redirect('users:signup')
    
    try:
        user = User.objects.create_user(username, email, password)
        user.save()
        user.profile.firstname = request.POST['firstname']
        user.profile.lastname = request.POST['lastname']
        user.profile.status = 'bu'
        user.save()
    
    except IntegrityError:
        messages.warning(request, 'pls choose another username, the username already exists')
        return redirect('users:signup')
    except ValueError:
        messages.warning(request, 'pls fill all the fields')
        return redirect('users:signup')
    
    return redirect('users:coreLogin')

def coreLogin(request):
    return render(request, 'registration/login.html')
            
@login_required
def dashboard(request):
    user = request.user
    ctx = {
        'user':user,
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
    return render(request, 'users/dashboardQuiz.html', ctx)

def coreLoginProcessor(request):
    if request.method == 'POST':
        
        try:
            username = request.POST['username']
            password = request.POST['password']
        
            if len(username)== 0:
                messages.error(request, "please fill all the fields")
                return redirect ('users:coreLogin')

            elif len(username)== 0:
                messages.error(request, "please fill all the fields")
                return redirect ('users:coreLogin')
        
            elif len(username) != 0 and len(password) == 0:
                messages.error(request, "pls fill in the password field")
                return redirect('users:coreLogin')
            elif len(password) !=0 and len(username) == 0:
                messages.error(request, "pls fill in the username field")
                return redirect ('users:coreLogin')
        
        except IntegrityError:
            messages.error(request, 'pls fill in the correct credentials')
            return redirect('users:coreLogin')
        
        try:
            user = authenticate(username=username, password=password)
            profile = Profile.objects.get_or_create(user = user)
    
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('index')
                else:
                    messages.warning(request, 'your account has been disabled temporarily, pls contact the admin')
            else:
                messages.warning(request, 'your account is not found in the database pls re-register')
                return redirect('users:coreLogin')
        except IntegrityError:
            messages.error(request, 'pls fill in the correct credentials')
            return redirect('users:coreLogin')