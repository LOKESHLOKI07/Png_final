from django import forms
from django.contrib.auth.hashers import make_password

from .models import *
from django.contrib.auth.forms import AuthenticationForm

# Form for company registration
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'email', 'logo', 'banner','banner_content', 'description','services', 'password','website_url','youtube_url', 'instagram_url', 'facebook_url','linkedin_url','title']

# Form for login, where email is used as the username
class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))  # Use email for login
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)

from django import forms
from django.contrib.auth.models import User

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Enter your registered email", max_length=254)
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)


from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'  # Include all fields, including password
        exclude = ['bullet_points']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Make password field a TextInput to display hashed password
    #     self.fields['password'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
    #
    #     # Add a custom Textarea widget for the bullet_points field
    #     self.fields['bullet_points'].widget = forms.Textarea(
    #         attrs={
    #             'id': 'bullet-textarea',
    #             'rows': 5,
    #             'placeholder': '* Type your first point\n* Press Enter for the next point',
    #         }
    #     )


# Recently Added Lines

class NewsForm(forms.ModelForm):
    class Meta:
        model = NewsUpload
        fields = ['news_img', 'title', 'content', 'author']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_img', 'name', 'location', 'description']