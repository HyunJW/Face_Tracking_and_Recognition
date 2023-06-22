from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    is_staff = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'age', 'gender', 'email',
                  'phone_number', 'address', 'profile_picture')


class CustomAdminUserCreationForm(CustomUserCreationForm):

    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields + ('is_staff',)
