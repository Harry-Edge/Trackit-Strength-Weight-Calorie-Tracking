from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm


class UserSignUpForm(UserCreationForm):

    username = forms.CharField(max_length=100, label="", required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}))

    first_name = forms.CharField(max_length=100, label="", required=False,
                                 widget=forms.TextInput
                                 (attrs={'class': 'form-control mb-3', 'placeholder': 'First Name'}))

    last_name = forms.CharField(max_length=100, label="", required=False,
                                widget=forms.TextInput
                                (attrs={'class': 'form-control mb-3', 'placeholder': 'Last Name'}))

    email = forms.CharField(max_length=100, label="", required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Email'}))

    password1 = forms.CharField(max_length=100, label="", required=False,
                                widget=forms.PasswordInput(attrs={'class': 'form-control mb-3',
                                                                  'placeholder': 'Password '}))
    password2 = forms.CharField(max_length=100, label="", required=False,
                                widget=forms.PasswordInput(attrs={'class': 'form-control mb-3',
                                                                  'placeholder': 'Re-enter Password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', "password2")


class UserProfileForm(UserChangeForm):

    password = None

    username = forms.CharField(max_length=100, label="",  widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', )
        password = None


class ChangePasswordForm(PasswordChangeForm):

    old_password = forms.CharField(max_length=100, label="",
                                   widget=forms.PasswordInput(attrs={'class': 'form-control mb-3',
                                                                     'type': 'password',
                                                                     'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(max_length=100, label="",
                                    widget=forms.PasswordInput(attrs={'class': 'form-control mb-3',
                                                                      'type': 'password',
                                                                      'placeholder': 'New Password'}))
    new_password2 = forms.CharField(max_length=100, label="",
                                    widget=forms.PasswordInput(attrs={'class': 'form-control mb-3',
                                                                      'type': 'password',
                                                                      'placeholder': 'Confirm New Password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')