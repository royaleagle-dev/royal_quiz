from django import forms

from quiz.models import MyUser

class SignupForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = '__all__'
        exclude = ['score', 'last_score', 'temp_question_range','highest_score','lowest_score', 'score_depo', 'most_recent_quiz',]
        #exclude score and last_score from signin form
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
#MyUser.firstname.widget.attrs.update({'class': 'form-control'})