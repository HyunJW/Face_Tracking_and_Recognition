from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import EmailField

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(label='전화번호', help_text='010-0000-0000 형식으로 입력하세요')
    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2', 'birthdate', 'gender', 'address', 'phone_number',
                  'profile_picture')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if self.instance and self.instance.invalid_phone(phone_number):
            raise forms.ValidationError("유효한 전화번호를 입력해주세요.")
        return phone_number


class LoginForm(AuthenticationForm):
    username = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))


class EditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'birthdate', 'gender', 'address', 'phone_number', 'profile_picture')
