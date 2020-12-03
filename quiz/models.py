from django.db import models
from django_random_queryset import RandomManager
import uuid
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length = 2000)
    pub_date = models.DateTimeField(auto_now = True)
    category = models.ForeignKey('Category', on_delete = models.SET_NULL, null = True, blank = True)
    subject = models.ForeignKey('Subject', on_delete = models.SET_NULL, null = True)
    objects = RandomManager()
    
    def __str__(self):
        return self.title
    
class Category(models.Model):
    title = models.CharField(max_length = 200,)
    
    def __str__(self):
        return self.title

class Subject(models.Model):
    category = models.ForeignKey('Category', on_delete = models.SET_NULL, null = True, blank = True)
    title = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.title

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice = models.CharField(max_length = 2000)
    flag = models.BooleanField(default = False)
    pub_date = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.choice


class News(models.Model):
    title = models.CharField(max_length = 1000)
    body = models.TextField(max_length = 10000)
    pub_date = models.DateTimeField(auto_now = True)
    author = models.CharField(max_length = 10, default = 'RoyalEagle Team', editable = False)

    def __str__(self):
        return self.title

class Contest(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 255)
    description = models.CharField(max_length = 2000)
    added = models.DateField(default = timezone.now)
    register_end = models.DateField(default = timezone.now)
    RP_requirement = models.IntegerField(default = 50)
    participants = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.id)