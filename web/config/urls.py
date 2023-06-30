from django.contrib import admin
from django.urls import include, path
from attendance.views import home, start, home_selected

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", start),
    path("home/", home),
    path("home_selected/", home_selected),

    path('user/', include('user.urls')),
    path('attendance/', include('attendance.urls')),
]

