from django.db import models
# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    date_of_birth= models.DateField(null = True, blank = True)
    firstname = models.CharField(max_length = 200)
    lastname = models.CharField(max_length = 200)
    added = models.DateTimeField(auto_now_add = True)
    score = models.IntegerField(default = 0)
    highest_score = models.CharField(max_length = 200)
    lowest_score = models.CharField(max_length = 200)
    temp_question_range = models.IntegerField(default = 0)
    most_recent_quiz = models.CharField(max_length = 200, default = '')
    date_done = models.DateTimeField(auto_now = True)
    score_depo = models.CharField(max_length = 10000)
    RP = models.IntegerField(default = 0)
    total_quiz_count = models.IntegerField(default = 0)
    total_question_answered = models.IntegerField(default = 0)
    counter = models.IntegerField(default = 0)
    current_questions_list = models.CharField(max_length = 2000, blank = True, null = True)
    attainable_score = models.IntegerField(default = 0)
    percentage_score = models.IntegerField(default = 0)
    mystatus = (
        ('bu', 'basic user'),
        ('au', 'advanced user'),
    )
    
    status = models.CharField(max_length = 3, choices = mystatus, blank = True, default = 'bu')    
    
    def __str__(self):
        fName = self.firstname
        lName = self.lastname
        fullName = fName + ' ' + lName
        return lName
    
    @receiver(post_save, sender = User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user= instance)
            
    @receiver(post_save, sender = User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        
    
class PendingQuestion(models.Model):
    question = models.CharField(max_length = 255)
    option1 = models.CharField(max_length = 255)
    option2 = models.CharField(max_length = 255)
    option3 = models.CharField(max_length = 255)
    option4 = models.CharField(max_length = 255)
    is_approved = models.BooleanField(default = False)
    sender = models.CharField(max_length = 255, editable = False)
    category = models.CharField(max_length = 255)
    subject = models.CharField(max_length = 255)
    answer = models.CharField(max_length = 255)
        
    def approved(self):
        if self.is_approved == True:
            return True
        else:
            return False
        
    def __str__ (self):
        return self.question
        