from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Profile, Project, Task, Comment


class UserRegisterForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Enter a valid email address.',
        validators=[EmailValidator(message=('Invalid email address'))]
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1',
                  'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        allowed_domains = ["gmail.com", "yahoo.com", "outlook.com"]
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email address already registered.')

        domain = email.split('@')[-1]
        if domain not in allowed_domains:
            raise ValidationError('Invalid email domain.')
        return email


class LoginForm(AuthenticationForm):
    """User login form"""
    username = forms.EmailField(label="Email")

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(
                self.request, username=email, password=password
                )
            if not user:
                raise ValidationError("Invalid email or password.")
        return super().clean()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_bio', 'status', 'user_img']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'end_date', 'team_member']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'project', 'assignee']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
