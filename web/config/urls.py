from django.contrib import admin
from django.urls import include, path
from attendance.views import home, start

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", start),
    path("home/", home),

    path('user/', include('user.urls')),
    path('attendance/', include('attendance.urls')),
]

