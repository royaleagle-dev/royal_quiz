from django import forms

from quiz.models import MyUser

class SignupForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = '__all__'
        exclude = ['score', 'last_score', 'temp_question_range']
        #exclude score and last_score from signin form