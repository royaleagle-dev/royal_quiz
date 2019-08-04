from django.contrib import admin

# Register your models here.

from quiz.models import Question, Choice, MyUser, Category, Subject

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(MyUser)
admin.site.register(Category)
admin.site.register(Subject)
