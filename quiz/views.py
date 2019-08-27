from django.shortcuts import render, get_object_or_404, redirect
from quiz.models import Question, Choice, Category, Subject
from users.models import Profile
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . forms import SignupForm
import random
from django.http import QueryDict
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.core.mail import BadHeaderError, send_mail



class CategoryListView(ListView):
    model = Category
    template_name = 'quiz/mycatlist.html'
    context_object_name = 'mycatlist'

def contact(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        from_mail = request.POST['email']
        if subject and message and from_mail:
            if len(subject) != 0 and len(message) !=0 and len(from_mail) !=0:
                try:
                    send_mail(subject, message, from_email, ['royaleagle.dev@gmail.com'])
                except BadHeaderError:
                    return HttpResponse ('Something went wrong pls try again')
                messages.success (request, 'suggestion successfully sent')
                return redirect('index')
            else:
                messages.warning(request, 'pls fill in all required field')
                return redirect('contact')
    else:
        return render(request, 'quiz/contact.html')
    
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
    'category':category,
    'category_count':category_count,
    'question_count':question_count,
    }
    return render(request, 'quiz/index.html', ctx)

@login_required
def quiz_param(request, subject):
    user = request.user
    question_range = int(user.profile.temp_question_range)
    user.profile.most_recent_quiz = str(subject)
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
    user = request.user
    user.profile.temp_question_range = total_question
    user.profile.score = 0
    user.save()
    associated_questions = Question.objects.filter(subject__title = subject)
    global question_id_list
    for item in associated_questions:
        question_id_list.append(item.id)
    return redirect('quiz_page', subject = subject, pk = random.choice(question_id_list))


def postProcessor(request):
    user = request.user
    score = int(user.profile.score)
    user.profile.score_depo += (str(score)+',')
    user.save()
    
    listOfScores = user.profile.score_depo
    y = str(listOfScores)
    x = y.split(sep = ',')
    temp = [ ]
    if len(temp) == 0:
        temp.append(int(0))
    for item in x:
        if item != ',':
            if item != '':
                temp.append(int(item))
    
    
    user.profile.highest_score = max(temp)
    user.profile.lowest_score = min(temp)
    user.save()
    return redirect('end_exam')



@login_required
def quiz_page(request, pk, subject):
    question = get_object_or_404(Question, pk = pk, subject__title = subject)
    choices = Choice.objects.filter(question__exact = question)
    user = request.user
    
    associated_question = Question.objects.filter(subject__title = subject)
    for item in associated_question:
        global question_id_list
        question_id_list.append(item.id)

     #sessions
    #number of visits to this view as counted in the session variable
    num_visits = request.session.get('num_visits',0)
    request.session ['num_visits'] = num_visits +1
    
    if num_visits == int(user.profile.temp_question_range):
        user = request.user
        user.profile.total_question_answered += num_visits
        user.save()
        user.profile.RP += (user.profile.total_question_answered/5)
        user.save()
        del request.session['num_visits']
        return redirect ('postProcessor')
    
    ctx = {
        'question':question,
        'choices':choices,
        'num_visits': num_visits,
        #'question_id_list': question_id_list
    }
    return render(request, 'quiz/quiz_page.html', ctx)


#work not yet done on this view.
@login_required
def mark(request, pk, subject):
    global question_id_list
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
        user = request.user
        #user_id = current_user.id
        #user = User.objects.get(id = user_id)
        #user_mark = MyUser.objects.get(username = user.username)
        user.profile.score += score
        user.save()
        user.profile.last_score = user.profile.score
        user.save()
        messages.success(request, " CORRECT! you scored {0}".format(score))
        return HttpResponseRedirect(reverse('quiz_page', args = [str(subject), str(next_question,)]))
    
    else:
        total_question = Question.objects.all().count()
        #next_question = random.choice(question_id_list)
        answer = 'incorrect'
        score = -10
        
        user = request.user
        #user_id = current_user.id
        #user = User.objects.get(id = user_id)
        #user_mark = MyUser.objects.get(username = user.username)
        
        user.profile.score += score
        user.save()
        user.profile.last_score = user.profile.score
        user.save()
        
        messages.error(request, "sorry incorrect answer")
        return HttpResponseRedirect(reverse('quiz_page', args = [str(subject), str(next_question,)]))
    
    
@login_required
def end_exam(request):
    return redirect('users:dashboard')