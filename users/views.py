from django.shortcuts import render, redirect
#from users.forms import SignupForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login
from users.models import Profile
from django.contrib.auth.decorators import login_required


# Create your views here.

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
    else:
        messages.warning(request, 'invalid login credentials-- either your password or your username is not correct')
        return redirect('users:login')
    

@login_required
def dashboard(request):
    user = request.user
    ctx = {
        'user':user,
    }
    return render(request, 'users/dashboard.html', ctx)

@login_required
def dashboardUsers(request):
    users = User.objects.all().order_by('-profile__RP')
    ctx = {
        'users':users
    }
    return render(request, 'users/dashboardUsers.html', ctx)