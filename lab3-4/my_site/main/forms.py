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

    def is_valid(self):
        valid = super().is_valid()

        if not valid:
            return valid

        if '-' in self.cleaned_data['title']:
            return False
        return True


class UpdateReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('title', 'text')

    def is_valid(self):
        valid = super().is_valid()

        if not valid:
            return valid

        if '-' in self.cleaned_data['title']:
            return False
        return True