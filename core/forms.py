from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task, Project

from .models import Task


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        min_length=4,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Логин'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2'
        ]

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Такой пользователь уже существует.'
            )

        return username


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select'
            }),

            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),

            'deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'project': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control'
            }),

            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }