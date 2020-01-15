from django.db import models

# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length = 2000)
    pub_date = models.DateTimeField(auto_now = True)
    category = models.ForeignKey('Category', on_delete = models.SET_NULL, null = True, blank = True)
    subject = models.ForeignKey('Subject', on_delete = models.SET_NULL, null = True)
    
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