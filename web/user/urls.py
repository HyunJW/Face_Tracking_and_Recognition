from django.urls import path
from user.views import (
    UserRegistrationView,
    UserLoginView,
    user_info,
    user_edit,
    password_update,
)
from django.contrib.auth.views import LogoutView
from attendance.views import user_class
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'

urlpatterns = [
    path('create/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('info/', user_info),
    path('info/update/', user_edit),
    path('info/update/password/', password_update),
    path('class/', user_class),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

