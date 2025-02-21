from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
class CustomUserCreationForm(UserCreationForm): 
    class Meta:
        model = User
        fields = ['first_name', 'email','username', 'password1', 'password2']
        labels = {
            'first_name': 'Name:',  # Custom field label
            'email': 'Email Address:',
            'username':'Username:',
            'password1': 'Password:',
            'password2': 'Confirm Password:',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'username': forms.TextInput(attrs={'class': 'form- control', 'placeholder': 'Enter Username'}),
            'password1':forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '.........'}),
            'password2':forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '.........'}),
        }
            
            
            
            
            
        
    def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)
            # updating the field class
            for name, field in self.fields.items():
                field.widget.attrs.update(
                        {'class':'input'}
                        )


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'location', 'email', 'phone', 'country']
    def __init__(self, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)
            # updating the field class
            for name, field in self.fields.items():
                field.widget.attrs.update(
                        {'class':'input'}
                        )