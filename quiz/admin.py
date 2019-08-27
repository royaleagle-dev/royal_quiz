from django.contrib import admin

# Register your models here.

from quiz.models import Question, Choice, Category, Subject

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'choice', 'flag']
    list_display_links = ('choice',)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    max_num = 4
    can_delete = False
    min_num =  1
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'subject']
    empty_value_display = "{{null}}"
    #fields = ('title', ('category', 'subject'))
    fieldsets = (('Question',{'fields': ('title',)}),
     ('Options', {
         'fields':(('category', 'subject'),)
     })
    )
    inlines = [ChoiceInline,]
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Category)
admin.site.register(Subject)
