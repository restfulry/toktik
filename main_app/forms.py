from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Answer, Question


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer', 'is_anon']


class QuestionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        label="", queryset=Question.objects.filter().values_list('category', flat=True), empty_label="Placeholder")

    class Meta:
        model = Question
        fields = ['question', 'category', 'is_anon']

        # widgets = {
        #     'question': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Start your question with "What", "How", "Why", etc'}),
        #     'category': forms.Select(attrs={'class': 'form-select form-select-lg', 'id': 'floatingSelectGrid'}),
        #     'is_anon': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        # }

        # labels = {
        #     'question': '',
        #     'category': '',
        #     'is_anon': 'Anonymous'
        # }
