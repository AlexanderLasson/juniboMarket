from django import forms
from .models import Product
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

    def check_password(self):
        if self.cleaned_data['password']!=self.cleaned_data['password2']:
            raise forms.ValidationError('Password Fields do not match')
        return self.cleaned_data['password2']