from django.shortcuts import render, get_object_or_404, redirect
from quiz.models import Question, Choice, MyUser
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . forms import SignupForm
import random

# Create your views here.

@login_required
def index_test(request):
    available_question = Question.objects.count()
    user = request.user
    current_user = User.objects.get(id = user.id)
    USER = MyUser.objects.get(username = current_user.username)
    user_score = USER.score
    USER.score = 0
    USER.save()
    ctx = {
    'available_question':available_question,
    #'user_score':user_score,
    'USER': USER
    }
    return render(request, 'quiz/index.html', ctx)



@login_required
def quiz_page(request, pk):
    question = get_object_or_404(Question, pk = pk)
    choices = Choice.objects.filter(question__exact = question)
    user = request.user
    current_user = User.objects.get(id = user.id)
    user_score = MyUser.objects.get(username = current_user.username)
    ctx = {
        'question':question,
        'choices':choices,
        'user_score':user_score
    }
    return render(request, 'quiz/quiz_page.html', ctx)

@login_required
def mark(request, pk):
    user = User()
    
    question = get_object_or_404(Question, pk = pk)
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
    if selected_choice.flag == True:
        answer = 'correct'
        score = 10
        current_user = request.user
        user_id = current_user.id
        user = User.objects.get(id = user_id)
        user_mark = MyUser.objects.get(username = user.username)
        user_mark.score += score
        user_mark.save()
        messages.success(request, " CORRECT! you scored {0}".format(score))
        
        total_question = Question.objects.all().count()
        incrementor = random.randrange(question.id, total_question+1)
        next_question = question.id+incrementor
        if next_question > total_question:
            next_question = total_question-question.id
            if next_question == 0:
                next_question = random.randrange(1, total_question)
        
        return HttpResponseRedirect(reverse('quiz_page', args = str(next_question)))
    else:
        total_question = Question.objects.all().count()
        incrementor = random.randrange(question.id, total_question+1)
        next_question = question.id+incrementor
        if next_question > total_question:
            next_question = total_question-question.id
            if next_question == 0:
                next_question = random.randrange(1, total_question)

        answer = 'incorrect'
        score = -10
        
        current_user = request.user
        user_id = current_user.id
        user = User.objects.get(id = user_id)
        user_mark = MyUser.objects.get(username = user.username)
        user_mark.score += score
        user_mark.save()
        
        messages.error(request, "sorry incorrect answer")
        return HttpResponseRedirect(reverse('quiz_page', args = str(next_question)))
    

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
            return redirect('login')
    else:
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form':form})
    
@login_required
def end_exam(request):
    user = request.user
    user = User.objects.get(id = user.id)
    user = MyUser.objects.get(username = user.username)
    score = user.score
    user.last_score = score
    user.save()
    return redirect('index_test')
    
        
