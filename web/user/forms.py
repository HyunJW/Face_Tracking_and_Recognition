from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.forms import EmailField
from django.contrib.auth.hashers import check_password

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
    GENDERS = (
        ('M', '남성'),
        ('W', '여성'),
    )
    password = None
    name = forms.CharField(label='이름', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '30', }),
                           )
    birthdate = forms.DateField(label='생년월일', widget=forms.DateInput(
        attrs={'class': 'form-control', }),
                                )
    gender = forms.ChoiceField(choices=GENDERS, label='성별', widget=forms.Select(
        attrs={'class': 'form-control', }),
                               )
    address = forms.CharField(label='주소', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '100', }),
                              )
    phone_number = forms.CharField(label='전화번호', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '20', }),
                                   )
    profile_picture = forms.ImageField(label='프로필 사진', required=False, widget=forms.ClearableFileInput(
        attrs={'class': 'form-control'}),
                                       )

    class Meta:
        model = User
        fields = ('name', 'birthdate', 'gender', 'address', 'phone_number')


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
        })
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })


class CheckPasswordForm(forms.Form):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control', }),
                               )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password

        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')
