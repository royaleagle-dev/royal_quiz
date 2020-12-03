from django.shortcuts import render, get_object_or_404, redirect
from quiz.models import Question, Choice, Category, Subject, Contest
from users.models import Profile
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . forms import SignupForm
#import random
from django.http import QueryDict
import datetime

#class django.views.generic.detail.DetailView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.core.mail import BadHeaderError, send_mail

def about(request):
    return render(request, 'quiz/about.html')

# Create your views here.
def index(request):
    return render(request, 'quiz/index.html')

class ContestListView(ListView):
    model = Contest
    template_name = 'quiz/contest.html'
    context_object_name = 'contest'

    def get_queryset(self):
        queryset = {'all': Contest.objects.all().order_by('-register_end')}
        return queryset


@login_required
def pre_quiz(request,):
    subjects = Subject.objects.all().order_by('-title')
    if request.method == 'POST':
        user = request.user
        selected_subject = request.POST.get('subject')
        temp_question_range = request.POST.get('range')
        timeRange = request.POST.get('timeRange')
        
        #start time
        startTime = datetime.datetime.today()
        year = startTime.year
        month = startTime.month
        day = startTime.day
        hour = startTime.hour
        minute = startTime.minute
        seconds = startTime.second
        
        #end time
        minute = minute+int(timeRange)
        if minute >= 60:
            minute = minute-60
            hour = hour + 1
        endtime = datetime.datetime(year, month, day, hour, minute, seconds)
        user.profile.endtime = endtime
        
        
        user.profile.timeRange = timeRange
        user.profile.temp_question_range = temp_question_range
        #user.profile.counter = user.profile.temp_question_range
        user.profile.attainable_score = 2 * int(user.profile.temp_question_range)
        user.profile.score = 0
        user.profile.correct_questions = 0
        user.profile.wrong_questions = 0
        #user.profile.current_questions_list = str(0)
        user.profile.most_recent_quiz = selected_subject
        user.save()
        questions = Question.objects.filter(subject__id__exact = selected_subject)
        
        '''
        for item in questions:
            user.profile.current_questions_list += (str(item.id)+',')
            user.save()
        '''
        return redirect('quiz_page', selected_subject = selected_subject)    
    else:
        ctx = {
        'subjects':subjects,
        }
        return render(request, 'quiz/quiz_param.html', ctx)

#import random
@login_required
def quiz_page(request, selected_subject):
    user = request.user
    #user.profile.counter -= 1
    #user.save()
    #total_question = str(user.profile.current_questions_list)
    #questions = total_question.split(',')

    #check if the user has answered the total questions
    #if user.profile.counter < 0:
    #    return redirect('postProcessor')
    
    #original question to be presented to the user each time (at random)
    
    real_question = Question.objects.filter(subject__exact = selected_subject).random(user.profile.temp_question_range) 
    '''
    real_question_id = random.choice(questions)
    if len(real_question_id) < 1:
        real_question_id = questions[0]
    real_question = Question.objects.get(id = real_question_id)'''

    #choices (4) for each randomly selected question.
    #choices = Choice.objects.filter(question__id__exact = real_question_id)

    
    ctx = {
        'real_question':real_question,
        #'choices':choices,
    }
    return render(request, 'quiz/quiz_page.html', ctx)


@login_required
def mark(request):
    user = request.user
    data = request.GET.get('choiceIds')
    answers_list = data.split(',')
    print(answers_list)
    for items in answers_list:
        choice = Choice.objects.get(id = int(items))
        if choice.flag == True:
            #answer is correct
            score = 2
            user.profile.score += score
            user.profile.correct_questions +=1
            user.profile.last_score = user.profile.score
            user.save()
        else:
            #answer is not correct
            score = 0
            user.profile.score +=0
            user.profile.wrong_questions +=1
            user.profile.last_score = user.profile.score
            user.save()
    return redirect('postProcessor')
        
def postProcessor(request):
    user = request.user
    score = int(user.profile.percentage_score)
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
    user.profile.total_question_answered += user.profile.temp_question_range 
    user.profile.total_quiz_count += 1
    user.profile.RP += 3
    user.profile.percentage_score = (int(user.profile.score) / int(user.profile.attainable_score)) * 100
    user.save()
    return redirect('end_exam')

@login_required
def end_exam(request):
    user = request.user
    subject = Subject.objects.get(id = user.profile.most_recent_quiz)
    return render(request, 'users/result.html', {'user':user,'subject':subject,})

from . models import News
class NewsListView(ListView):
    model = News
    template_name = 'quiz/news.html'
    context_object_name = 'news'
    queryset = News.objects.all().order_by('-title')
