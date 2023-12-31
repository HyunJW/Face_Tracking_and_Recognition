from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, update_session_auth_hash, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from user.forms import UserRegistrationForm, LoginForm, EditForm, CustomPasswordChangeForm, CheckPasswordForm
from django.contrib import messages
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.messages.views import SuccessMessageMixin

User = get_user_model()


def login_message_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "로그인한 사용자만 이용할 수 있습니다.")
            return redirect(settings.LOGIN_URL)
        return function(request, *args, **kwargs)
    return wrap


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = '/user/login'
    success_message = "회원가입이 완료되었습니다."

    def form_valid(self, form):
        user = form.save(commit=False)
        profile_picture = form.cleaned_data['profile_picture']
        extension = profile_picture.name.split('.')[-1]

        user.save()
        user_id = str(user.id)

        new_filename = f'{user_id}.{extension}'
        media_root = settings.MEDIA_ROOT
        media_path = os.path.join(media_root, new_filename)

        with open(media_path, 'wb') as f:
            for chunk in profile_picture.chunks():
                f.write(chunk)

        if user.profile_picture.name:
            default_storage.delete(user.profile_picture.path)

        user.profile_picture.name = f'profile_pictures/{new_filename}'
        user.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'user/login_form.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)


@login_message_required
def user_info(request):
    return render(request, 'user/info.html')


@login_message_required
def user_edit(request):
    user_change_form = EditForm(instance=request.user)
    if request.method == 'POST':
        user_change_form = EditForm(request.POST, request.FILES, instance=request.user)
        if user_change_form.is_valid():
            profile_picture = request.FILES.get('profile_picture')

            if profile_picture:
                user_id = str(request.user.id)
                extension = profile_picture.name.split('.')[-1]
                new_filename = f'{user_id}.{extension}'
                media_root = settings.MEDIA_ROOT
                media_path = os.path.join(media_root, new_filename)

                with open(media_path, 'wb') as f:
                    for chunk in profile_picture.chunks():
                        f.write(chunk)

                if request.user.profile_picture:
                    default_storage.delete(request.user.profile_picture.path)

                request.user.profile_picture.name = f'profile_pictures/{new_filename}'
                request.user.save()

            user_change_form.save()

            messages.success(request, '회원정보가 수정되었습니다.')
            return render(request, 'user/info.html')

    return render(request, 'user/info_update.html', {'user_change_form': user_change_form})


@login_message_required
def password_update(request):
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return render(request, 'user/info.html')
    else:
        password_change_form = CustomPasswordChangeForm(request.user)

    return render(request, 'user/password_update.html', {'password_change_form': password_change_form})


@login_message_required
def user_delete(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)

        if password_form.is_valid():
            profile_picture_path = os.path.join(settings.MEDIA_ROOT, str(request.user.profile_picture).split('/')[-1])
            if os.path.isfile(profile_picture_path):
                os.remove(profile_picture_path)

            request.user.delete()
            logout(request)
            messages.success(request, "회원탈퇴가 완료되었습니다.")
            return redirect('/user/login/')
    else:
        password_form = CheckPasswordForm(request.user)

    return render(request, 'user/user_delete.html', {'password_form': password_form})
