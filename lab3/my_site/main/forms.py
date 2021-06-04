from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review


class SignupForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class CreateReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('title', 'text')