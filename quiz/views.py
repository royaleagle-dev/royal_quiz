from django.shortcuts import render, get_object_or_404, redirect
from quiz.models import Question, Choice, MyUser, Category, Subject
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . forms import SignupForm
import random
from django.http import QueryDict
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login

@login_required
def dashboard(request):
    current_user = request.user
    current_user = MyUser.objects.get(username = current_user.username)
    ctx = {
        'current_user':current_user
    }
    return render(request, 'quiz/dashboard.html', ctx)

def mylogin(request):
    return render(request, 'quiz/mlogin.html')

def login_processor(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    current_url = request.POST.get('next')
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return redirect('index')
    else:
        messages.warning(request, 'invalid login credentials')
        return redirect('mylogin')
    

class CategoryListView(ListView):
    model = Category
    template_name = 'quiz/mycatlist.html'
    context_object_name = 'mycatlist'

def contact(request):
    return render (request, 'quiz/contact.html')

def robots(request):
    return render(request, 'quiz/robots.txt')

question_id_list = [ ]

# Create your views here.
def index(request):
    category_count = Category.objects.all().count()
    question_count = Question.objects.all().count()
    category = Category.objects.all()
    available_question = Question.objects.count()
    global question_id_list
    question_id_list = []
    
    ctx = {
    'available_question':available_question,
    #'USER': USER,
    'category':category,
    'category_count':category_count,
    'question_count':question_count,
    }
    return render(request, 'quiz/index.html', ctx)

@login_required
def quiz_param(request, subject):
    current_user = request.user
    user = MyUser.objects.get(username = current_user.username)    
    question_range = int(user.temp_question_range)
    user.most_recent_quiz = str(subject)
    user.save()
    ctx = {
        'subject':subject
    }
    return render(request, 'quiz/quiz_param.html', ctx)


def category_detail(request, category):
    section = Subject.objects.filter(category__title__exact = category)
    question_count = Question.objects.filter(category__title__exact = category).count()
    ctx = {
        'category':category,
        'question_count':question_count,
        'section': section
    }
    return render(request, 'quiz/category_detail.html', ctx)


def process(request, subject):
    total_question = request.POST.get('tot_quiz_question', False)
    total_question = int(total_question)
    current_user = request.user
    user = MyUser.objects.get(username = current_user.username)
    user.temp_question_range = total_question
    user.score = 0
    user.save()
    associated_questions = Question.objects.filter(subject__title = subject)
    global question_id_list
    for item in associated_questions:
        question_id_list.append(item.id)
    return redirect('quiz_page', subject = subject, pk = random.choice(question_id_list))


def postProcessor(request):
    current_user = request.user
    user = MyUser.objects.get(username = current_user.username)
    score = int(user.score)
    user.score_depo += (str(score)+',')
    user.save()
    
    listOfScores = user.score_depo
    y = str(listOfScores)
    x = y.split(sep = ',')
    temp = [ ]
    if len(temp) == 0:
        temp.append(int(0))
    for item in x:
        if item != ',':
            if item != '':
                temp.append(int(item))
    
    
    user.highest_score = max(temp)
    user.lowest_score = min(temp)
    user.save()
    return redirect('end_exam')



@login_required
def quiz_page(request, pk, subject):
    question = get_object_or_404(Question, pk = pk, subject__title = subject)
    choices = Choice.objects.filter(question__exact = question)
    user = request.user
    current_user = User.objects.get(id = user.id)
    user = MyUser.objects.get(username = current_user.username)
    user_score = MyUser.objects.get(username = current_user.username)
    
    associated_question = Question.objects.filter(subject__title = subject)
    for item in associated_question:
        global question_id_list
        question_id_list.append(item.id)

     #sessions
    #number of visits to this view as counted in the session variable
    num_visits = request.session.get('num_visits',0)
    request.session ['num_visits'] = num_visits +1
    
    if num_visits == int(user.temp_question_range):
        del request.session['num_visits']
        return redirect ('postProcessor')
    
    ctx = {
        'question':question,
        'choices':choices,
        'user_score':user_score,
        'num_visits': num_visits,
        #'question_id_list': question_id_list
    }
    return render(request, 'quiz/quiz_page.html', ctx)


#work not yet done on this view.
@login_required
def mark(request, pk, subject):
    global question_id_list
    user = User()
    
    question = get_object_or_404(Question, pk = pk)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        messages.warning(request, 'you do not choose any option')
        return redirect ('quiz_page', pk = random.choice(question_id_list), subject = subject)
    
    associated_question = Question.objects.filter(subject__title = subject)
    for items in associated_question:
        #global question_id_list
        question_id_list.append(items.id)
        
    next_question = random.choice(question_id_list)
        
    if selected_choice.flag == True:
        answer = 'correct'
        score = 10
        current_user = request.user
        user_id = current_user.id
        user = User.objects.get(id = user_id)
        user_mark = MyUser.objects.get(username = user.username)
        user_mark.score += score
        user_mark.save()
        user.last_score = user_mark.score
        user_mark.save()
        messages.success(request, " CORRECT! you scored {0}".format(score))
        return HttpResponseRedirect(reverse('quiz_page', args = [str(subject), str(next_question,)]))
    
    else:
        total_question = Question.objects.all().count()
        #next_question = random.choice(question_id_list)
        answer = 'incorrect'
        score = -10
        
        current_user = request.user
        user_id = current_user.id
        user = User.objects.get(id = user_id)
        user_mark = MyUser.objects.get(username = user.username)
        
        user_mark.score += score
        user_mark.save()
        user.last_score = user_mark.score
        user_mark.save()
        
        messages.error(request, "sorry incorrect answer")
        return HttpResponseRedirect(reverse('quiz_page', args = [str(subject), str(next_question,)]))
    

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid:
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = User.objects.create_user(username, email, password)
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.save()
            messages.success(request, 'User Created Successfully')
            return redirect('mlogin')
    else:
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form':form})
    
@login_required
def end_exam(request):
    return redirect('dashboard')