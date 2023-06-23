from django.contrib import admin
from attendance.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'email', 'name', 'age', 'gender', 'phone_number', 'address', 'profile_picture',
                    'date_joined', 'is_staff', 'is_active', 'last_login')
    list_display_links = ('user_id', 'email')
    exclude = ('password',)

    def date_joined(self, obj):
        return obj.date_joined.strftime("%Y-%m-%d")

    def last_login(self, obj):
        if not obj.last_login:
            return ''
        return obj.last_login.strftime("%Y-%m-%d %H:%M")

    date_joined.admin_order_field = '-date_joined'  # 가장 최근에 가입한 사람부터 리스팅
    date_joined.short_description = '가입일'
    last_login.admin_order_field = 'last_login_at'
    last_login.short_description = '최근로그인'