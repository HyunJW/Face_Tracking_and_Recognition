from django.contrib import admin
from attendance.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'first_name', 'last_name', 'age', 'gender', 'email', 'phone_number',
                    'address', 'profile_picture', 'date_joined', 'is_staff', 'is_active', 'last_login')


admin.site.register(User, UserAdmin)
